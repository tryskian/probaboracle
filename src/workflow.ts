import { Agent, run } from "@openai/agents";

import { probaboracleConfig, type QuestionType } from "./config/index.js";

export type WorkflowInput = { question_type: QuestionType };

export type WorkflowOutput = { output_text: string };

const workflowConfig = probaboracleConfig.workflow;
type GenerationMeta = {
  model: string;
  prompt_frame: string;
  provider: string;
};

export type WorkflowDebug = {
  generation_meta: GenerationMeta;
};

const resolveModelName = (): string =>
  process.env[workflowConfig.model.modelEnvVar] ?? workflowConfig.model.defaultName;

const ensureApiKey = (): void => {
  if (!process.env[workflowConfig.model.apiKeyEnvVar]) {
    throw new Error(
      `Set ${workflowConfig.model.apiKeyEnvVar} before running Probaboracle.`
    );
  }
};

const buildPrompt = (question_type: QuestionType, prompt_frame: string): string =>
  [
    workflowConfig.inputTemplate,
    `Prompt type: ${question_type}`,
    `Prompt frame: ${prompt_frame}`
  ].join("\n");

const buildAgent = (model: string): Agent =>
  new Agent({
    name: "Probaboracle",
    instructions: workflowConfig.instructions,
    model,
    modelSettings: {
      temperature: workflowConfig.model.temperature,
      maxTokens: workflowConfig.model.maxTokens,
      store: workflowConfig.model.store,
      reasoning: workflowConfig.model.reasoning,
      text: workflowConfig.model.text
    }
  });

const normaliseOutputText = (value: string): string => {
  let output = value.trim();

  if (workflowConfig.render.trimQuotes) {
    output = output.replace(/^["'“”]+|["'“”]+$/g, "");
  }

  if (workflowConfig.render.collapseWhitespace) {
    output = output.replace(/\s+/g, " ").trim();
  }

  return output;
};

const expectOutputText = (value: unknown): string => {
  if (typeof value !== "string") {
    throw new Error("Probaboracle agent did not return text output.");
  }

  const output = normaliseOutputText(value);

  if (!output) {
    throw new Error("Probaboracle agent returned empty output.");
  }

  return output;
};

export const runWorkflow = async (
  workflow: WorkflowInput
): Promise<WorkflowOutput & WorkflowDebug> => {
  ensureApiKey();

  const prompt_frame = workflowConfig.promptFrames[workflow.question_type];
  const model = resolveModelName();
  const agent = buildAgent(model);
  const result = await run(
    agent,
    buildPrompt(workflow.question_type, prompt_frame)
  );
  const output_text = expectOutputText(result.finalOutput);

  return {
    output_text,
    generation_meta: {
      model,
      prompt_frame,
      provider: workflowConfig.provider
    }
  };
};

export const debugPipeline = {
  config: workflowConfig,
  buildPrompt,
  resolveModelName
};
