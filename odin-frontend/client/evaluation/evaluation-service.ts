import {
  DatasetSimilarity,
  fetchSimilarityMethods,
  SimilarityMethod,
} from "../app-service/similarity-api";
import {
  getSimilarDatasets,
  FetchOptions,
} from "../app-service/similarity-service";
import {fetchEvaluationGroup } from "../app-service/evaluation-api";
import {Dataset} from "../app-service/dataset-api";

export {postEvaluation} from "../app-service/evaluation-api";

export interface SimilarForGroupResponse {
  method: MethodData[];
  datasets: { [iri: string]: Dataset };
  description: string;
}

interface MethodData {
  method: SimilarityMethod;
  datasets: DatasetSimilarity[],
  numberOfDatasets: number,
  numberOfDatasetsWithSameScoreAsTheLast: number,
}

export async function getSimilarForGroup(
  evaluationGroupName: string,
  queryDatasets: string[],
  options: FetchOptions): Promise<SimilarForGroupResponse> {
  const evaluationGroups = await fetchEvaluationGroup(evaluationGroupName);
  const methodsMetadata = await fetchSimilarityMethods();
  const methods = evaluationGroups.methods
    .map(name => methodsMetadata[name])
    .filter(item => item !== undefined);
  const response = await getSimilarDatasets(methods, queryDatasets, options);
  const result:SimilarForGroupResponse = {
    "method": [],
    "datasets": response.datasets,
    "description": evaluationGroups.description,
  };
  for (const [key, data] of Object.entries(response.similar)) {
    result.method.push({
      ...data,
      "method" : methodsMetadata[key],
    });
  }
  return result;
}

export function shuffleArray(array: any[]) {
  // Special care for array of size two.
  if (array.length == 2) {
    if (Math.random() > 0.5) {
      [array[0], array[1]] = [array[1], array[0]];
    }
    return;
  }
  // Swap randomly position of each element with some other.
  for (let index = array.length - 1; index > 0; index--) {
    const swapWithIndex = Math.floor(Math.random() * (index + 1));
    [array[index], array[swapWithIndex]] = [array[swapWithIndex], array[index]];
  }
}
