export class MappingData {
    id: string;
    group: string;
    shared: number;
    size: number;

    constructor (id: string, group: string, shared: number, size: number) {
      this.group = group
      this.id = id
      this.shared = shared
      this.size = size
    }
}
