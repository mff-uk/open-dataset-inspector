export interface MappingNode {
    id: number;
    nodeID?: string;
    mapBy?: string;
    name: string;
    children?: MappingNode[];
}
