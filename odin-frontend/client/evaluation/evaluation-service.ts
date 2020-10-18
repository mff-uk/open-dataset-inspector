import {getEvaluationGroup} from "./evaluation-api";
import {
  SimilarityResponse,
  getSimilarToDataset,
  DatasetPosition,
  getDatasetsPositions,
  PositionResponse,
} from "./similarity-api";
import {Dataset, getDataset} from "./dataset-api";

export {postEvaluation} from "./evaluation-api";

export interface MethodData extends SimilarityResponse {
  id: string;
}

export interface FetchSimilarDatasets {
  methods: MethodData[];
  datasets: { [iri: string]: Dataset };
  description: string;
}

export interface FetchOptions {
  count: number;
  fusion?: string,
}

export interface FetchMoreForMethod {
  method: MethodData,
  datasets: { [iri: string]: Dataset };
}

export type FetchDatasetsPosition = { [method: string]: DatasetPosition[] };

export async function fetchSimilarDatasets(
  evaluationGroupName: string,
  queryDatasets: string[],
  options: FetchOptions): Promise<FetchSimilarDatasets> {
  const evaluationGroups = await getEvaluationGroup(evaluationGroupName);
  const result: FetchSimilarDatasets = {
    "methods": [],
    "datasets": {},
    "description": evaluationGroups.description,
  };
  const fusion: string = options.fusion || evaluationGroups.fusion || "min";
  const referencedDatasets: Set<string> = new Set();
  if (queryDatasets.length > 0) {
    for (let methodId of evaluationGroups.methods) {
      try {
        const methodData: MethodData = {
          "id": methodId,
          ...await getSimilarToDataset(
            methodId, queryDatasets, fusion, options.count)
        };
        methodData.datasets.forEach((item) => {
          referencedDatasets.add(item.iri);
        });
        result.methods.push(methodData);
      } catch (ex) {
        console.error("Missing similarity record.", ex);
      }
    }
  }
  for (let datasetIri of queryDatasets) {
    referencedDatasets.add(datasetIri);
  }
  result.datasets = await fetchDatasets(Array.from(referencedDatasets));
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

export async function fetchDatasets(datasets: string[])
  : Promise<{ [iri: string]: Dataset }> {
  //
  const result: { [iri: string]: Dataset } = {};
  for (let datasetIri of datasets) {
    try {
      result[datasetIri] = await getDataset(datasetIri);
    } catch (ex) {
      console.error("Missing dataset detail.", ex);
    }
  }
  return result;
}

export async function fetchMoreForMethod(
  method: string, queryDatasets: string[], knowDatasets: string[],
  options: FetchOptions): Promise<FetchMoreForMethod> {
  //
  const fusion = options.fusion || "max";
  const methodData: MethodData = {
    "id": method,
    ...await getSimilarToDataset(
      method, queryDatasets, fusion, options.count)
  };
  const datasetsToFetch = methodData.datasets
    .map((dataset) => dataset.iri)
    .filter((iri) => !knowDatasets.includes(iri));
  return {
    "method": methodData,
    "datasets": await fetchDatasets(Array.from(datasetsToFetch))
  };
}

export async function fetchDatasetsPositions(
  evaluationGroupName: string,
  queryDatasets: string[],
  datasets: string[],
  fusion?: string): Promise<FetchDatasetsPosition> {
  const evaluationGroups = await getEvaluationGroup(evaluationGroupName);
  const result: FetchDatasetsPosition = {};
  const fusionToUse: string = fusion || evaluationGroups.fusion || "min";
  if (queryDatasets.length > 0) {
    for (let methodId of evaluationGroups.methods) {
      try {
        const positions: PositionResponse =
          await getDatasetsPositions(
            methodId, queryDatasets, fusionToUse, datasets);
        result[methodId] = positions.datasets;
      } catch (ex) {
        console.error("Missing similarity record.", ex);
      }
    }
  }
  return result;
}
