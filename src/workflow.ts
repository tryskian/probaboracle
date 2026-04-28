import { probaboracleConfig, type QuestionType } from "./config/index.js";

export type WorkflowInput = { question_type: QuestionType };

export type WorkflowOutput = { output_text: string };

const workflowConfig = probaboracleConfig.workflow;
const pick = <T>(items: readonly T[]): T =>
  items[Math.floor(Math.random() * items.length)]!;

const chance = (probability: number): boolean => Math.random() < probability;

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

type ResponseParts = {
  anchor: string;
  body: string;
};

export type WorkflowDebug = {
  response_parts: ResponseParts;
};

const laneNodes = workflowConfig.nodes.lanes;

const buildBody = (question_type: QuestionType): string => {
  const lane = laneNodes[question_type];
  const segments: string[] = [pick(lane.bases)];

  if (chance(workflowConfig.render.addWobbleChance)) {
    segments.push(`${pick(workflowConfig.nodes.connectiveHinges)} ${pick(lane.wobbles)}`);
  }

  if (chance(workflowConfig.render.addSoftConclusionChance)) {
    segments.push(pick(workflowConfig.nodes.softConclusions));
  }

  return segments.join(", ");
};

const buildResponseParts = (question_type: QuestionType): ResponseParts => ({
  anchor: pick(workflowConfig.nodes.certaintyWords),
  body: buildBody(question_type)
});

export const runWorkflow = async (
  workflow: WorkflowInput
): Promise<WorkflowOutput & WorkflowDebug> => {
  const response_parts = buildResponseParts(workflow.question_type);
  const output_text = normaliseOutputText(
    `${response_parts.anchor} ${response_parts.body}.`
  );

  return {
    output_text,
    response_parts
  };
};

export const debugPipeline = {
  config: workflowConfig,
  buildResponseParts
};
