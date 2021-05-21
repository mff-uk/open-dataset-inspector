import axios from "axios";

export interface EvaluationGroup {
  datasets: string[];
  explanation: object[];
}

export function fetchExplanation(
  method: string, left: string, right: string): Promise<EvaluationGroup> {
  const url = `./api/v1/similarity/explain/${method}`
    + "?dataset=" + encodeURIComponent(left)
    + "&dataset=" + encodeURIComponent(right);
  return axios.get(url).then((response) => response.data);
}
