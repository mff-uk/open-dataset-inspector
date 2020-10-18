export function queryParamsToDatasetString(value: string | string []): string {
  if (value === undefined) {
    return "";
  }
  if (Array.isArray(value)) {
    return value.join("\n");
  }
  return value;
}

export function datasetStringToArray(
  datasetString: string | undefined): string[] {
  if (datasetString === undefined) {
    return [];
  }
  return String(datasetString).split(/\s+/).filter(Boolean);
}
