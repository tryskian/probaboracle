import { join } from "node:path";

export const questionTypes = ["what", "when", "how", "why", "where"] as const;

export type QuestionType = (typeof questionTypes)[number];

export const evalVerdicts = ["pass", "fail"] as const;

export type EvalVerdict = (typeof evalVerdicts)[number];

export const productConfig = {
  outputLanguage: "en-GB",
  promptTypes: questionTypes
} as const;

export const cliConfig = {
  defaultQuestionType: "what" as QuestionType,
  defaultEvalSampleCount: 10,
  defaultEvalListLimit: 20
} as const;

export const storageConfig = {
  evalDbRelativePath: [".probaboracle", "evals.sqlite"] as const
} as const;

export const resolveEvalDbPath = (cwd: string): string =>
  join(cwd, ...storageConfig.evalDbRelativePath);
