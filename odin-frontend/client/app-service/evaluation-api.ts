import axios from "axios";

export interface EvaluationGroup {
  methods: string[];
  description: string;
  fusion?: string;
}

export function fetchEvaluationGroup(
  groupName: string): Promise<EvaluationGroup> {
  const url = `./api/v1/evaluation/${groupName}`;
  return axios.get(url).then((response) => response.data);
}

export async function postEvaluation(evaluation: object) {
  const url = "./api/v1/evaluation";
  return axios.post(url, evaluation);
}
