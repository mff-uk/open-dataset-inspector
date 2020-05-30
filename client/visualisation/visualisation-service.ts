
type Filter<T> = (T: any) => boolean;

export interface MappingFilterOptions {
  directlyMapped: boolean;
  userFilterFunction?: string;
  compiledUserFilterFunction?: Filter<any>;
}

export interface HighlightFilterOptions {
  directlyMapped: boolean;
  usedInPaths: boolean;
}

export interface PathOptions {
  method: string;
  distance: number;
  autoFetch: boolean;
}

export interface Path {
  shared: string;
  nodes: string[];
}

export function createDefaultMappingOptions() : MappingFilterOptions {
  return {
    "directlyMapped": true,
  };
}

export function createDefaultHighlightFilterOptions() : HighlightFilterOptions {
  return {
    "directlyMapped": false,
    "usedInPaths": true,
  }
}

export function createDefaultPathOptions() : PathOptions {
  return {
    "method": "distance",
    "distance": 1,
    "autoFetch": true,
  }
}

export function createMappingFilters(options: MappingFilterOptions) {
  const filters: Filter<any>[] = [];

  if (options.directlyMapped) {
    filters.push(filterDirectlyMappedMappings);
  }

  if (options.compiledUserFilterFunction) {
    filters.push(options.compiledUserFilterFunction);
  }

  return (mappings: any[]) => {
    return mappings.map((mapping: any) => {
      return {
        ...mapping,
        "data": mapping.data.filter((mapping: any) => {
          for (const check of filters) {
            if (!check(mapping)) {
              return false;
            }
          }
          return true;
        }),
      }
    });
  };
}

const filterDirectlyMappedMappings =
  (mapping: any) => mapping.metadata.directly_mapped;

export function createHighlightsFilter(
  paths: Path[] | undefined, options: HighlightFilterOptions) {
  const filters: Filter<String>[] = [];
  const usedInPaths = new Set();

  if (paths !== undefined && options.usedInPaths) {
    paths.forEach(
      (path) => path.nodes.forEach(
        (node) => usedInPaths.add(node)));
    filters.push((node) => usedInPaths.has(node));
  }

  const applyFilters : Filter<String> = (item:string) => {
    for (const filter of filters) {
      if (!filter(item)) {
        return false;
      }
    }
    return true;
  }

  return (items: String[])=> {
    const filtered = items.filter(applyFilters);
    return new Set(filtered)
  };
}

