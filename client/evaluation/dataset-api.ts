import axios from "axios";

export interface Dataset {
  iri: string;
  title: string;
  description: string;
  keywords: string[];
}

export function getDataset(datasetIri: string): Promise<Dataset> {
  const url = "./api/v1/dataset?dataset=" + encodeURIComponent(datasetIri);
  return axios.get(url).then((response) => response.data);
}
