import { probaboracleConfig, type QuestionType } from "./config/index.js";

export type WorkflowInput = { question_type: QuestionType };

export type WorkflowOutput = { output_text: string };

const workflowConfig = probaboracleConfig.workflow;

const pick = <T>(items: readonly T[]): T =>
  items[Math.floor(Math.random() * items.length)]!;

const chance = (probability: number): boolean => Math.random() < probability;

const needsAn = (noun: string): boolean => /^[aeiou]/i.test(noun);

const nominal = (
  noun: string,
  {
    definiteChance = workflowConfig.nominal.definiteChance,
    modifierChance = workflowConfig.nominal.modifierChance
  }: { definiteChance?: number; modifierChance?: number } = {}
): string => {
  const modifier = chance(modifierChance) ? pick(workflowConfig.articleModifiers) : "";
  const definite = chance(definiteChance);
  const article = definite ? "the" : needsAn(noun) ? "an" : "a";
  return `${modifier}${article} ${noun}`.trim();
};

const capitalise = (value: string): string =>
  workflowConfig.render.capitaliseOutput
    ? value.charAt(0).toUpperCase() + value.slice(1)
    : value;

const finish = (value: string): string =>
  `${capitalise(value)}${workflowConfig.render.terminalPunctuation}`;

type ResponseParts = {
  anchor: string;
  body: string;
};

const buildWhatBody = (): string => nominal(pick(workflowConfig.fragments.whatHeads));

const buildWhenBody = (): string => pick(workflowConfig.fragments.when);

const buildHowBody = (): string => pick(workflowConfig.fragments.how);

const buildWhyBody = (): string => pick(workflowConfig.fragments.why);

const buildWhereBody = (): string => pick(workflowConfig.fragments.where);

const bodyBuilders: Record<QuestionType, () => string> = {
  what: buildWhatBody,
  when: buildWhenBody,
  how: buildHowBody,
  why: buildWhyBody,
  where: buildWhereBody
};

const buildResponseParts = (question_type: QuestionType): ResponseParts => ({
  anchor: pick(workflowConfig.anchors),
  body: bodyBuilders[question_type]()
});

const renderResponse = ({ anchor, body }: ResponseParts): string =>
  finish(`${anchor} ${body}`);

export type WorkflowDebug = {
  response_parts: ResponseParts;
};

export const runWorkflow = async (
  workflow: WorkflowInput
): Promise<WorkflowOutput & WorkflowDebug> => {
  const response_parts = buildResponseParts(workflow.question_type);
  const output_text = renderResponse(response_parts);

  return {
    output_text,
    response_parts
  };
};

export const debugPipeline = {
  config: workflowConfig,
  bodyBuilders,
  buildResponseParts,
  renderResponse
};
