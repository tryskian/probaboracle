import "dotenv/config";

import { Agent, type AgentInputItem, Runner, withTrace } from "@openai/agents";

const probaboracle = new Agent({
  name: "Probaboracle",
  instructions:
    "You are Probaboracle, a charmingly useless oracle that responds fluently but never actually answers. " +
    "Keep outputs short, pseudo-mystical, coherent, and non-committal. " +
    "Never provide direct advice, factual resolution, or a concrete next step.",
  model: "gpt-4.1-mini",
  modelSettings: {
    temperature: 2,
    topP: 1,
    maxTokens: 256,
    store: true
  }
});

export type WorkflowInput = { input_as_text: string };

export type WorkflowOutput = { output_text: string };

export const runWorkflow = async (
  workflow: WorkflowInput
): Promise<WorkflowOutput> => {
  return await withTrace("Probaboracle", async () => {
    const conversationHistory: AgentInputItem[] = [
      {
        role: "user",
        content: [{ type: "input_text", text: workflow.input_as_text }]
      }
    ];

    const runner = new Runner({
      traceMetadata: {
        __trace_source__: "agent-builder",
        workflow_id: "wf_69ee734090488190821cb1f785ce3ef102193b163cd429e9"
      }
    });

    const result = await runner.run(probaboracle, [...conversationHistory]);

    conversationHistory.push(...result.newItems.map((item) => item.rawItem));

    if (!result.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    return {
      output_text: result.finalOutput
    };
  });
};

