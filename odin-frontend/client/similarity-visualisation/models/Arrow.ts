export class Arrow {
    id: number;
    word?: string;
    mapTo?: string;
    lx: number;
    ly: number;
    rx: number;
    ry: number;
    r: number;

    constructor (id: number, lx: number, ly: number, rx: number, ry: number, r: number, word?: string, mapTo?: string) {
      this.id = id
      this.lx = lx
      this.ly = ly
      this.rx = rx
      this.ry = ry
      this.r = r
      this.word = word
      this.mapTo = mapTo
    }
}
