export const workflowConfig = {
  version: "semantic-node-pipeline-v1",
  provider: "local",
  nodes: {
    certaintyWords: [
      "Certainly",
      "Technically",
      "Arguably",
      "Probably",
      "Definitely",
      "Most likely"
    ],
    connectiveHinges: ["but", "though", "except", "only", "and yet"],
    softConclusions: [
      "which settles very little",
      "so make of that what you will",
      "though that hardly helps",
      "and that's about all there is to it"
    ],
    lanes: {
      what: {
        bases: [
          "something of that kind",
          "a thing of that sort",
          "not exactly one clear thing",
          "the general category, more or less"
        ],
        wobbles: [
          "not by much",
          "not cleanly",
          "not very convincingly",
          "not in any settled way"
        ]
      },
      when: {
        bases: [
          "too early",
          "too late",
          "off by a moment",
          "not at the ideal time"
        ],
        wobbles: [
          "not by much",
          "not in a helpful way",
          "not exactly on time",
          "not when it would have counted"
        ]
      },
      how: {
        bases: [
          "in some kind of order",
          "by a method that sounds better than it works",
          "through a process",
          "in steps, more or less"
        ],
        wobbles: [
          "not clearly",
          "not very well",
          "not in a useful way",
          "not in any clean sequence"
        ]
      },
      why: {
        bases: [
          "for reasons unclear",
          "because that seems to be the reason",
          "for some reason",
          "because that is apparently the point"
        ],
        wobbles: [
          "not a very satisfying one",
          "not one that clarifies much",
          "not in any convincing sense",
          "not without some doubt"
        ]
      },
      where: {
        bases: [
          "somewhere nearby",
          "elsewhere",
          "on the other side of things",
          "in the general area"
        ],
        wobbles: [
          "not anywhere useful",
          "not very precisely",
          "not close enough to settle it",
          "not in a way that helps much"
        ]
      }
    }
  },
  render: {
    collapseWhitespace: true,
    trimQuotes: true,
    addSoftConclusionChance: 0.2,
    addWobbleChance: 0.65
  }
} as const;
