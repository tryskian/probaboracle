export type QuestionType = "what" | "when" | "how" | "why" | "where";

export type WorkflowInput = { question_type: QuestionType };

export type WorkflowOutput = { output_text: string };

const classifiers = {
  anchors: [
    "Certainly",
    "Technically",
    "Arguably",
    "Probably",
    "Definitely",
    "Most likely"
  ] as const,
  articleModifiers: ["", "not quite ", "hardly "] as const,
  turns: {
    what: ["but what"],
    when: ["but when"],
    how: ["but how"],
    why: ["but why"],
    where: ["but where"]
  } as const,
  whatHeads: ["maybe", "answer", "toss-up", "thing"] as const,
  whenFragments: [
    "too early",
    "too late",
    "not yet",
    "already over",
    "at the wrong time",
    "past the point",
    "off by a moment"
  ] as const,
  howFragments: [
    "in steps",
    "by some method",
    "in no clear order",
    "through a process",
    "in rough order"
  ] as const,
  whyFragments: [
    "for some reason",
    "for no clear reason",
    "for reasons unclear",
    "because that is apparently the point",
    "because that seems to be the reason"
  ] as const,
  whereFragments: [
    "nearby",
    "elsewhere",
    "on the other side",
    "not far away",
    "nowhere useful",
    "in the general area"
  ] as const
};

const pick = <T>(items: readonly T[]): T =>
  items[Math.floor(Math.random() * items.length)]!;

const chance = (probability: number): boolean => Math.random() < probability;

const needsAn = (noun: string): boolean => /^[aeiou]/i.test(noun);

const nominal = (
  noun: string,
  {
    definiteChance = 0.3,
    modifierChance = 0.25
  }: { definiteChance?: number; modifierChance?: number } = {}
): string => {
  const modifier = chance(modifierChance) ? pick(classifiers.articleModifiers) : "";
  const definite = chance(definiteChance);
  const article = definite ? "the" : needsAn(noun) ? "an" : "a";
  return `${modifier}${article} ${noun}`.trim();
};

const capitalise = (value: string): string =>
  value.charAt(0).toUpperCase() + value.slice(1);

const finish = (value: string): string => `${capitalise(value)}.`;

type ResponseParts = {
  anchor: string;
  body: string;
};

const buildWhatBody = (): string => nominal(pick(classifiers.whatHeads));

const buildWhenBody = (): string => pick(classifiers.whenFragments);

const buildHowBody = (): string => pick(classifiers.howFragments);

const buildWhyBody = (): string => pick(classifiers.whyFragments);

const buildWhereBody = (): string => pick(classifiers.whereFragments);

const bodyBuilders: Record<QuestionType, () => string> = {
  what: buildWhatBody,
  when: buildWhenBody,
  how: buildHowBody,
  why: buildWhyBody,
  where: buildWhereBody
};

const buildResponseParts = (question_type: QuestionType): ResponseParts => ({
  anchor: pick(classifiers.anchors),
  body: bodyBuilders[question_type]()
});

const renderResponse = ({ anchor, body }: ResponseParts): string =>
  finish(`${anchor} ${body}`);

export const runWorkflow = async (
  workflow: WorkflowInput
): Promise<WorkflowOutput> => {
  const output_text = renderResponse(buildResponseParts(workflow.question_type));

  return {
    output_text
  };
};

export const debugPipeline = {
  classifiers,
  bodyBuilders,
  buildResponseParts,
  renderResponse
};
