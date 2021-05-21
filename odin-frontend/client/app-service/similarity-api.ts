import axios from "axios";

export interface SimilarityMethod {
  id: string;
  paired: boolean;
  explanation: string;
  label: string;
  fusion: string;
}

export type SimilarityMethodsResponse = Record<string, SimilarityMethod>;

export async function fetchSimilarityMethods()
  : Promise<SimilarityMethodsResponse> {
  const url = "./api/v1/similarity";
  const response = await axios.get(url);
  const data = response.data.data;
  const result: SimilarityMethodsResponse = {};
  for (const [key, value] of Object.entries(data)) {
    result[key] = {
      // @ts-ignore
      ...value,
      "id": key,
    };
  }
  return result;
}

export interface SimilarToDatasetResponse {
  datasets: DatasetSimilarity[],
  numberOfDatasets: number,
  numberOfDatasetsWithSameScoreAsTheLast: number,
}

export interface DatasetSimilarity {
  iri: string;
  score: number;
}

export function fetchSimilarToDataset(
  similarity: SimilarityMethod,
  queryDatasets: string[],
  count: number): Promise<SimilarToDatasetResponse> {
  const url = `./api/v1/similarity/search/${similarity.id}` +
    "?fusion=" + similarity.fusion + "&count=" + count + "&query=" +
    queryDatasets.map(encodeURIComponent).join("&query=");
  return axios.get(url).then((response) => response.data);
}

export interface DatasetPositionResponse {
  datasets: DatasetPosition[];
  totalNumberOfDatasets: number;
}

export interface DatasetPosition extends DatasetSimilarity {
  score: number;
  positionMin: number;
  positionMax: number;
}

export function fetchDatasetsPositions(
  similarity: SimilarityMethod,
  queryDatasets: string[],
  datasetsToFind: string[],
): Promise<DatasetPositionResponse> {
  const url = `./api/v1/similarity/position/${similarity.id}` +
    "?fusion=" + similarity.fusion + "&query=" +
    queryDatasets.map(encodeURIComponent).join("&query=") + "&dataset=" +
    datasetsToFind.map(encodeURIComponent).join("&dataset=");
  return axios.get(url)
    .then((response) => response.data);
}