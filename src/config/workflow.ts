export const workflowConfig = {
  version: "classifier-pipeline-v2",
  anchors: [
    "Certainly",
    "Technically",
    "Arguably",
    "Probably",
    "Definitely",
    "Most likely"
  ],
  articleModifiers: ["", "not quite ", "hardly "],
  nominal: {
    definiteChance: 0.3,
    modifierChance: 0.25
  },
  render: {
    capitaliseOutput: true,
    terminalPunctuation: "."
  },
  fragments: {
    whatHeads: ["maybe", "answer", "toss-up", "thing"],
    when: [
      "too early",
      "too late",
      "not yet",
      "already over",
      "at the wrong time",
      "past the point",
      "off by a moment"
    ],
    how: [
      "in steps",
      "by some method",
      "in no clear order",
      "through a process",
      "in rough order"
    ],
    why: [
      "for some reason",
      "for no clear reason",
      "for reasons unclear",
      "because that is apparently the point",
      "because that seems to be the reason"
    ],
    where: [
      "nearby",
      "elsewhere",
      "on the other side",
      "not far away",
      "nowhere useful",
      "in the general area"
    ]
  }
} as const;
