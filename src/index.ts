import { runWorkflow } from "./workflow.js";

const input_as_text =
  process.argv.slice(2).join(" ").trim() || "what question: what is this, really?";

const result = await runWorkflow({ input_as_text });

console.log(result.output_text);
