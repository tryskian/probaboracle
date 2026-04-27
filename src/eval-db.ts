import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { randomUUID } from "node:crypto";

import {
  evalVerdicts,
  probaboracleConfig,
  resolveEvalDbPath,
  type EvalVerdict,
  type QuestionType
} from "./config/index.js";
import type { WorkflowDebug, WorkflowOutput } from "./workflow.js";

type SQLiteModule = typeof import("node:sqlite");

type DatabaseSync = InstanceType<SQLiteModule["DatabaseSync"]>;

export type EvalOutputRecord = WorkflowOutput &
  WorkflowDebug & {
    question_type: QuestionType;
  };

export type { EvalVerdict } from "./config/index.js";

export type EvalListRow = {
  output_id: number;
  run_id: string;
  ordinal: number;
  question_type: QuestionType;
  model: string;
  output_text: string;
  prompt_frame: string;
  verdict: EvalVerdict | null;
  note: string | null;
  created_at: string;
};

const DB_PATH = resolveEvalDbPath(process.cwd());
const GENERATOR_VERSION = probaboracleConfig.workflow.version;
const VERDICT_SQL_LIST = evalVerdicts.map((verdict) => `'${verdict}'`).join(", ");

const ensureEvalDir = (): void => {
  mkdirSync(dirname(DB_PATH), { recursive: true });
};

const loadSqlite = async (): Promise<SQLiteModule> => {
  const originalEmitWarning = process.emitWarning.bind(process);

  process.emitWarning = ((warning: string | Error, ...args: unknown[]) => {
    const message =
      typeof warning === "string"
        ? warning
        : warning instanceof Error
          ? warning.message
          : String(warning);
    const warningType = typeof args[0] === "string" ? args[0] : "";
    const isSqliteExperimentalWarning =
      warningType === "ExperimentalWarning" && message.includes("SQLite");

    if (!isSqliteExperimentalWarning) {
      return originalEmitWarning(
        warning as Parameters<typeof process.emitWarning>[0],
        ...(args as [])
      );
    }
  }) as typeof process.emitWarning;

  try {
    return await import("node:sqlite");
  } finally {
    process.emitWarning = originalEmitWarning;
  }
};

const openDb = async (): Promise<DatabaseSync> => {
  ensureEvalDir();
  const { DatabaseSync } = await loadSqlite();
  return new DatabaseSync(DB_PATH);
};

const readColumns = (
  db: DatabaseSync,
  tableName: string
): Array<{ name: string; type: string }> =>
  db.prepare(`PRAGMA table_info(${tableName})`).all() as Array<{
    name: string;
    type: string;
  }>;

const migrateSchema = (db: DatabaseSync): void => {
  const runColumns = readColumns(db, "eval_runs");
  const outputColumns = readColumns(db, "eval_outputs");
  const judgmentColumns = readColumns(db, "eval_judgments");

  const runSchemaOutdated =
    runColumns.length > 0 && !runColumns.some((column) => column.name === "model");

  const outputSchemaOutdated =
    outputColumns.length > 0 &&
    (outputColumns.some((column) => column.name === "anchor") ||
      outputColumns.some((column) => column.name === "body") ||
      !outputColumns.some((column) => column.name === "prompt_frame"));

  const judgmentSchemaOutdated =
    judgmentColumns.length > 0 &&
    !judgmentColumns.some((column) => column.name === "output_id");

  if (runSchemaOutdated || outputSchemaOutdated || judgmentSchemaOutdated) {
    db.exec(`
      DROP TABLE IF EXISTS eval_judgments;
      DROP TABLE IF EXISTS eval_outputs;
      DROP TABLE IF EXISTS eval_runs;
    `);
  }
};

const createSchema = (db: DatabaseSync): void => {
  migrateSchema(db);

  db.exec(`
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS eval_runs (
      id TEXT PRIMARY KEY,
      created_at TEXT NOT NULL,
      question_type TEXT NOT NULL,
      sample_count INTEGER NOT NULL,
      generator_version TEXT NOT NULL,
      model TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS eval_outputs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      run_id TEXT NOT NULL REFERENCES eval_runs(id) ON DELETE CASCADE,
      ordinal INTEGER NOT NULL,
      question_type TEXT NOT NULL,
      output_text TEXT NOT NULL,
      prompt_frame TEXT NOT NULL,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS eval_judgments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      output_id INTEGER NOT NULL UNIQUE REFERENCES eval_outputs(id) ON DELETE CASCADE,
      verdict TEXT NOT NULL
        CHECK (verdict IN (${VERDICT_SQL_LIST})),
      note TEXT NOT NULL DEFAULT '',
      created_at TEXT NOT NULL
    );
  `);
};

export const initEvalDatabase = async (): Promise<{ dbPath: string }> => {
  const db = await openDb();
  try {
    createSchema(db);
  } finally {
    db.close();
  }

  return { dbPath: DB_PATH };
};

export const recordEvalSampleRun = async (
  questionType: QuestionType,
  outputs: EvalOutputRecord[]
): Promise<{ dbPath: string; runId: string; outputIds: number[] }> => {
  const db = await openDb();
  const runId = randomUUID();
  const createdAt = new Date().toISOString();
  const outputIds: number[] = [];

  try {
    createSchema(db);

    const insertRun = db.prepare(`
      INSERT INTO eval_runs (
        id,
        created_at,
        question_type,
        sample_count,
        generator_version,
        model
      ) VALUES (?, ?, ?, ?, ?, ?)
    `);

    const insertOutput = db.prepare(`
      INSERT INTO eval_outputs (
        run_id,
        ordinal,
        question_type,
        output_text,
        prompt_frame,
        created_at
      ) VALUES (?, ?, ?, ?, ?, ?)
    `);

    db.exec("BEGIN");
    try {
      insertRun.run(
        runId,
        createdAt,
        questionType,
        outputs.length,
        GENERATOR_VERSION,
        outputs[0]?.generation_meta.model ?? "unknown"
      );

      outputs.forEach((output, index) => {
        const insertResult = insertOutput.run(
          runId,
          index + 1,
          output.question_type,
          output.output_text,
          output.generation_meta.prompt_frame,
          createdAt
        ) as { lastInsertRowid: number | bigint };

        outputIds.push(Number(insertResult.lastInsertRowid));
      });
      db.exec("COMMIT");
    } catch (error) {
      db.exec("ROLLBACK");
      throw error;
    }
  } finally {
    db.close();
  }

  return {
    dbPath: DB_PATH,
    runId,
    outputIds
  };
};

export const listEvalOutputs = async (
  options: {
    questionType?: QuestionType;
    limit?: number;
  } = {}
): Promise<{ dbPath: string; rows: EvalListRow[] }> => {
  const db = await openDb();

  try {
    createSchema(db);

    const limit = Math.max(1, options.limit ?? 20);
    const baseSelect = `
      SELECT
        eo.id AS output_id,
        eo.run_id,
        eo.ordinal,
        eo.question_type,
        er.model,
        eo.output_text,
        eo.prompt_frame,
        ej.verdict,
        ej.note,
        eo.created_at
      FROM eval_outputs eo
      JOIN eval_runs er
        ON er.id = eo.run_id
      LEFT JOIN eval_judgments ej
        ON ej.output_id = eo.id
    `;

    const rows = options.questionType
      ? (db
          .prepare(
            `
              ${baseSelect}
              WHERE eo.question_type = ?
              ORDER BY eo.id DESC
              LIMIT ?
            `
          )
          .all(options.questionType, limit) as EvalListRow[])
      : (db
          .prepare(
            `
              ${baseSelect}
              ORDER BY eo.id DESC
              LIMIT ?
            `
          )
          .all(limit) as EvalListRow[]);

    return {
      dbPath: DB_PATH,
      rows
    };
  } finally {
    db.close();
  }
};

export const judgeEvalOutput = async (
  outputId: number,
  verdict: EvalVerdict,
  note = ""
): Promise<{ dbPath: string; outputId: number; verdict: EvalVerdict }> => {
  const db = await openDb();
  const createdAt = new Date().toISOString();

  try {
    createSchema(db);

    const outputExists = db
      .prepare(`SELECT id FROM eval_outputs WHERE id = ?`)
      .get(outputId) as { id: number } | undefined;

    if (!outputExists) {
      throw new Error(`No eval output found for id ${outputId}`);
    }

    const deleteJudgment = db.prepare(`
      DELETE FROM eval_judgments
      WHERE output_id = ?
    `);

    const insertJudgment = db.prepare(`
      INSERT INTO eval_judgments (output_id, verdict, note, created_at)
      VALUES (?, ?, ?, ?)
    `);

    db.exec("BEGIN");
    try {
      deleteJudgment.run(outputId);
      insertJudgment.run(outputId, verdict, note, createdAt);
      db.exec("COMMIT");
    } catch (error) {
      db.exec("ROLLBACK");
      throw error;
    }

    return {
      dbPath: DB_PATH,
      outputId,
      verdict
    };
  } finally {
    db.close();
  }
};
