export class Path {
  from: string;
  to: string;
  vertices: Array<string>;
  up: number;
  down: number;
  height: number;
  arrows: Array<string>;
  leftKeywords: string;
  rightKeywords: string;

  constructor (from: string, to: string, vertices: Array<string>,
    up: number, down: number, height: number, arrows: Array<string>,
    leftKeywords: string, rightKeywords: string) {
    this.from = from
    this.to = to
    this.vertices = vertices
    this.up = up
    this.down = down
    this.height = height
    this.arrows = arrows
    this.leftKeywords = leftKeywords
    this.rightKeywords = rightKeywords
  }
}
