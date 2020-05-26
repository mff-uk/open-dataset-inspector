import axios from "axios";

export async function fetchDatasetHierarchy(
  collection: string, datasetUrl: string): Promise<object> {
  const url =
    "./api/v1/mapping/" + collection +
    "?dataset=" + encodeURIComponent(datasetUrl);
  const response = await axios.get(url);
  return response.data;
}

export async function fetchLabels(ids: Array<string>): Promise<object> {
  const url = "./api/v1/wikidata/labels";
  const response = await axios.post(url, ids);
  const result: Record<string, string> = {};
  response.data.data.labels.forEach((item:any) => {
    result[item.id] = item.label;
  });
  return result;
}


