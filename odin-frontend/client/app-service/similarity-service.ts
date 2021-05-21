import {
  SimilarToDatasetResponse,
  fetchSimilarToDataset,
  DatasetPosition,
  fetchDatasetsPositions,
  DatasetPositionResponse,
  SimilarityMethod,
} from "./similarity-api";
import {Dataset, fetchDataset} from "./dataset-api";

export interface SimilarDatasetsResponse {
  similar: { [method: string]: SimilarToDatasetResponse };
  datasets: { [iri: string]: Dataset };
}

export interface FetchOptions {
  count: number;
}

export async function getSimilarDatasets(
  methods: SimilarityMethod[],
  queryDatasets: string[],
  options: FetchOptions): Promise<SimilarDatasetsResponse> {
  //
  const result: SimilarDatasetsResponse = {
    "similar": {},
    "datasets": {},
  };
  const referencedDatasets: Set<string> = new Set();
  if (queryDatasets.length > 0) {
    for (const method of methods) {
      try {
        const similarDatasets = await fetchSimilarToDataset(
          method, queryDatasets, options.count);
        // Add to results.
        result.similar[method.id] = similarDatasets;
        // Add to all datasets so we can fetch them later.
        similarDatasets.datasets.forEach((item) => {
          referencedDatasets.add(item.iri);
        });
      } catch (ex) {
        console.error("Can't fetch similarity data.", ex);
      }
    }
  }
  for (let datasetIri of queryDatasets) {
    referencedDatasets.add(datasetIri);
  }
  result.datasets = await fetchDatasets(Array.from(referencedDatasets));
  return result;
}

async function fetchDatasets(datasets: string[])
  : Promise<{ [iri: string]: Dataset }> {
  //
  const result: { [iri: string]: Dataset } = {};
  for (let datasetIri of datasets) {
    try {
      result[datasetIri] = await fetchDataset(datasetIri);
    } catch (ex) {
      console.error("Missing dataset detail.", ex);
    }
  }
  return result;
}

export interface MoreSimilarDatasetsResponse {
  similar: SimilarToDatasetResponse;
  datasets: { [iri: string]: Dataset };
}

export async function getMoreSimilarDatasets(
  method: SimilarityMethod,
  queryDatasets: string[],
  knowDatasets: string[],
  options: FetchOptions): Promise<MoreSimilarDatasetsResponse> {
  //
  const similar =
    await fetchSimilarToDataset(method, queryDatasets, options.count);
  const datasetsToFetch = similar.datasets
    .map((dataset) => dataset.iri)
    .filter((iri) => !knowDatasets.includes(iri));
  return {
    "similar": similar,
    "datasets": await fetchDatasets(Array.from(datasetsToFetch))
  };
}

export type DatasetsPositionResponse =
  { [method: string]: DatasetPosition[] };

export async function getDatasetsPositions(
  methods: SimilarityMethod[],
  queryDatasets: string[],
  datasets: string[]): Promise<DatasetsPositionResponse> {
  const result: DatasetsPositionResponse = {};
  if (queryDatasets.length > 0) {
    for (let method of methods) {
      try {
        const positions: DatasetPositionResponse =
          await fetchDatasetsPositions(method, queryDatasets, datasets);
        result[method.id] = positions.datasets;
      } catch (ex) {
        console.error("Missing similarity record.", ex);
      }
    }
  }
  return result;
}
