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

export async function fetchSimilarity(
  options: any, left: any, right: any) : Promise<Object> {
  const url = "./api/v1/mapping-similarity";
  const form = new FormData();
  form.append("dataset", createDatasetBlob(left));
  form.append("dataset", createDatasetBlob(right));
  form.append("options", createJsonBlob(options));
  const response = await axios.post(url, form, {
    "headers": {
      "Content-Type": "multipart/form-data"
    }
  })
  return response.data;
}

function createDatasetBlob(dataset:any) {
  return createJsonBlob({
    "@id": dataset.url,
    "mappings": dataset.mappings,
    "hierarchy": dataset.hierarchy,
  });
}

function createJsonBlob(content:any) {
  return new Blob(
    [JSON.stringify(content)],
    { "type": "application/json" }
  );
}
