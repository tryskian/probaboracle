import "dotenv/config";

import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

import {
  initEvalDatabase,
  judgeEvalOutput,
  listEvalOutputs,
  recordEvalSampleRun
} from "./eval-db.js";
import {
  evalVerdicts,
  probaboracleConfig,
  questionTypes,
  type EvalVerdict,
  type QuestionType
} from "./config/index.js";
import { runWorkflow } from "./workflow.js";

const cliArgs = process.argv.slice(2);
const command = cliArgs[0]?.trim().toLowerCase();

const toQuestionType = (value: string | undefined): QuestionType =>
  questionTypes.includes(value as QuestionType)
    ? (value as QuestionType)
    : probaboracleConfig.cli.defaultQuestionType;

const toVerdict = (value: string | undefined): EvalVerdict => {
  if (evalVerdicts.includes(value as EvalVerdict)) {
    return value as EvalVerdict;
  }

  throw new Error(`Verdict must be one of: ${evalVerdicts.join(", ")}`);
};

const promptForVerdict = async (): Promise<EvalVerdict> => {
  const readline = createInterface({ input, output });

  try {
    while (true) {
      const answer = (await readline.question("Verdict [pass/fail]: "))
        .trim()
        .toLowerCase();

      if (answer === "p") {
        return "pass";
      }

      if (answer === "f") {
        return "fail";
      }

      if (evalVerdicts.includes(answer as EvalVerdict)) {
        return answer as EvalVerdict;
      }

      console.log("Enter pass or fail.");
    }
  } finally {
    readline.close();
  }
};

if (command === "eval:init") {
  const { dbPath } = await initEvalDatabase();
  console.log(`Initialised eval database at ${dbPath}`);
  process.exit(0);
}

if (command === "eval:sample") {
  const question_type = toQuestionType(cliArgs[1]?.trim().toLowerCase());
  const sampleCount = Math.max(
    1,
    Number.parseInt(
      cliArgs[2] ?? String(probaboracleConfig.cli.defaultEvalSampleCount),
      10
    ) || probaboracleConfig.cli.defaultEvalSampleCount
  );
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

if (command === "eval:prompt") {
  const question_type = toQuestionType(cliArgs[1]?.trim().toLowerCase());
  const result = await runWorkflow({ question_type });
  const { outputIds } = await recordEvalSampleRun(question_type, [
    {
      question_type,
      ...result
    }
  ]);

  const outputId = outputIds[0];

  if (!outputId) {
    throw new Error("Could not persist eval output for manual judging.");
  }

  console.log(result.output_text);
  const verdict = await promptForVerdict();
  await judgeEvalOutput(outputId, verdict);
  console.log(`Saved ${verdict} for output ${outputId}`);
  process.exit(0);
}

if (command === "eval:list") {
  const maybeQuestionType = cliArgs[1]?.trim().toLowerCase();
  const questionType = questionTypes.includes(maybeQuestionType as QuestionType)
    ? (maybeQuestionType as QuestionType)
    : undefined;
  const rawLimit = questionType ? cliArgs[2] : cliArgs[1];
  const limit = Math.max(
    1,
    Number.parseInt(
      rawLimit ?? String(probaboracleConfig.cli.defaultEvalListLimit),
      10
    ) || probaboracleConfig.cli.defaultEvalListLimit
  );
  const { dbPath, rows } = await listEvalOutputs({
    questionType,
    limit
  });

  console.log(`Listing ${rows.length} outputs from ${dbPath}`);
  rows.forEach((row) => {
    const verdict = row.verdict ?? "untagged";
    const note = row.note ? ` | ${row.note}` : "";
    console.log(
      `${row.output_id}. [${row.question_type} | ${row.model}] ${row.output_text} | ${verdict}${note}`
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
