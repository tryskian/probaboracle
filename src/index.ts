import {
  initEvalDatabase,
  judgeEvalOutput,
  listEvalOutputs,
  recordEvalSampleRun,
  type EvalVerdict
} from "./eval-db.js";
import { runWorkflow, type QuestionType } from "./workflow.js";

const allowedQuestionTypes: QuestionType[] = ["what", "when", "how", "why", "where"];
const allowedVerdicts: EvalVerdict[] = ["pass", "fail"];
const cliArgs = process.argv.slice(2);
const command = cliArgs[0]?.trim().toLowerCase();

const toQuestionType = (value: string | undefined): QuestionType =>
  allowedQuestionTypes.includes(value as QuestionType)
    ? (value as QuestionType)
    : "what";

const toVerdict = (value: string | undefined): EvalVerdict => {
  if (allowedVerdicts.includes(value as EvalVerdict)) {
    return value as EvalVerdict;
  }

  throw new Error(`Verdict must be one of: ${allowedVerdicts.join(", ")}`);
};

if (command === "eval:init") {
  const { dbPath } = await initEvalDatabase();
  console.log(`Initialised eval database at ${dbPath}`);
  process.exit(0);
}

if (command === "eval:sample") {
  const question_type = toQuestionType(cliArgs[1]?.trim().toLowerCase());
  const sampleCount = Math.max(1, Number.parseInt(cliArgs[2] ?? "10", 10) || 10);
  const outputs = [];

  for (let index = 0; index < sampleCount; index += 1) {
    const result = await runWorkflow({ question_type });
    outputs.push({
      question_type,
      ...result
    });
  }

  const { dbPath, runId } = await recordEvalSampleRun(question_type, outputs);

  console.log(`Stored run ${runId} in ${dbPath}`);
  outputs.forEach((output, index) => {
    console.log(`${index + 1}. ${output.output_text}`);
  });
  process.exit(0);
}

if (command === "eval:list") {
  const maybeQuestionType = cliArgs[1]?.trim().toLowerCase();
  const questionType = allowedQuestionTypes.includes(maybeQuestionType as QuestionType)
    ? (maybeQuestionType as QuestionType)
    : undefined;
  const rawLimit = questionType ? cliArgs[2] : cliArgs[1];
  const limit = Math.max(1, Number.parseInt(rawLimit ?? "20", 10) || 20);
  const { dbPath, rows } = await listEvalOutputs({
    questionType,
    limit
  });

  console.log(`Listing ${rows.length} outputs from ${dbPath}`);
  rows.forEach((row) => {
    const verdict = row.verdict ?? "untagged";
    const note = row.note ? ` | ${row.note}` : "";
    console.log(
      `${row.output_id}. [${row.question_type}] ${row.output_text} | ${verdict}${note}`
    );
  });
  process.exit(0);
}

if (command === "eval:judge") {
  const outputId = Number.parseInt(cliArgs[1] ?? "", 10);

  if (!Number.isInteger(outputId) || outputId < 1) {
    throw new Error("eval:judge requires a positive output id");
  }

  const verdict = toVerdict(cliArgs[2]?.trim().toLowerCase());
  const note = cliArgs.slice(3).join(" ").trim();
  const result = await judgeEvalOutput(outputId, verdict, note);

  console.log(`Judged output ${result.outputId} as ${result.verdict}`);
  process.exit(0);
}

const question_type = toQuestionType(command);
const result = await runWorkflow({ question_type });

console.log(result.output_text);
