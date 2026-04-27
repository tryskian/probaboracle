import { runWorkflow, type QuestionType } from "./workflow.js";

const allowedQuestionTypes: QuestionType[] = ["what", "when", "how", "why", "where"];
const cliValue = process.argv[2]?.trim().toLowerCase();
const question_type: QuestionType = allowedQuestionTypes.includes(
  cliValue as QuestionType
)
  ? (cliValue as QuestionType)
  : "what";

const result = await runWorkflow({ question_type });

console.log(result.output_text);
