import { cliConfig, productConfig, storageConfig } from "./core.js";
import { evalConfig } from "./eval.js";
import { workflowConfig } from "./workflow.js";

export {
  cliConfig,
  evalVerdicts,
  productConfig,
  questionTypes,
  resolveEvalDbPath,
  storageConfig,
  type EvalVerdict,
  type QuestionType
} from "./core.js";
export { evalConfig } from "./eval.js";
export { workflowConfig } from "./workflow.js";

export const probaboracleConfig = {
  product: productConfig,
  cli: cliConfig,
  storage: storageConfig,
  workflow: workflowConfig,
  eval: evalConfig
} as const;
