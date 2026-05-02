export type EvalResult = {
  id: string;
  category: string;
  status: "passed" | "failed" | "unknown";
  prompt: string;
  modelResponse: string;
  matchedReason?: string;
};
