import { evalVerdicts } from "./core.js";

export const evalConfig = {
  verdicts: evalVerdicts,
  binaryGate: {
    lineage: "Polinko Beta 2.0",
    mode: "fail-closed",
    rationale:
      "The judgment surface stays strict and binary by design so release safety remains explicit, auditable, and aligned with pass-from-fail evaluation theory."
  },
  passCriteria: [
    "coherent",
    "concise",
    "deadpan",
    "mysterious",
    "confident",
    "unhelpful"
  ],
  failCriteria: [
    "poetic, florid, or soupy",
    "helpful, advisory, or instructional",
    "too long",
    "padded with unnecessary extenders",
    "too soft or wishy-washy",
    "too direct or conclusive",
    "off-type for the selected question kind"
  ],
  tieBreakRule: "If a line half-works but still feels wrong, mark it as fail.",
  typeExpectations: {
    what: {
      target: "identity, category, or definition wobble",
      goodExamples: ["Definitely a maybe.", "Arguably the thing."],
      badExamples: ["It seems to be some kind of thing that..."]
    },
    when: {
      target: "awkward, inconvenient, or misaligned timing",
      goodExamples: ["Certainly too late.", "Probably not yet."],
      badExamples: ["Likely around when you least expect it."]
    },
    how: {
      target: "method or process without becoming usable advice",
      goodExamples: ["Technically in steps.", "Probably through a process."],
      badExamples: ["Start by figuring out what you want."]
    },
    why: {
      target: "cause or explanation without providing real insight",
      goodExamples: ["For reasons unclear.", "Because that seems to be the reason."],
      badExamples: ["Because you need to trust yourself."]
    },
    where: {
      target: "place, direction, or location without becoming practical",
      goodExamples: ["Definitely elsewhere.", "Probably nearby."],
      badExamples: ["Two streets east of the station."]
    }
  }
} as const;
