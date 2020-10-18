import axios from "axios";

export interface SimilarityResponse {
  datasets: DatasetSimilarity[],
  numDatasets: number,
  numSameScoreAsLast: number,
}

export interface DatasetSimilarity {
  iri: string;
  score: number;
}

export function getSimilarToDataset(
  similarityName: string,
  queryDatasets: string[],
  fusion: string,
  count: number): Promise<SimilarityResponse> {
  const url = `./api/v1/similarity/similar/${similarityName}` +
    "?fusion=" + fusion + "&count=" + count + "&query=" +
    queryDatasets.map(encodeURIComponent).join("&query=");
  return axios.get(url).then((response) => response.data);
}

export interface PositionResponse {
  datasets: DatasetPosition[];
}

export interface DatasetPosition extends DatasetSimilarity {
  positionMin: number;
  positionMax: number;
}

export function getDatasetsPositions(
  similarityName: string,
  queryDatasets: string[],
  fusion: string,
  datasets: string[],
): Promise<PositionResponse> {
  const url = `./api/v1/similarity/position/${similarityName}` +
    "?fusion=" + fusion + "&query=" +
    queryDatasets.map(encodeURIComponent).join("&query=") + "&dataset=" +
    datasets.map(encodeURIComponent).join("&dataset=");
  return axios.get(url)
    .then((response) => response.data);
}