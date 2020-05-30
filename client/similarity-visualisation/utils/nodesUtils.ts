import { ROOT_ID, Node, Link, Circle, Arrow, TREE_CIRCLE_RADIUS, ComboboxItem, Label } from '../models'
import * as d3 from 'd3'

function stringArrayContainsNodeById (array: Array<string>, id: string) {
  if (array.includes(id)) {
    return true
  } else {
    return false
  }
}

export function createLabel (id: string, label: string) {
  return {
    id: id,
    label: label
  }
}

export function mapLinks (links: any) {
  const result: Array<Link> = links.map((item: any) => ({
    parent: item[2],
    child: item[0]
  }))
  return result
}

// eslint-disable-next-line
export function addMappingItemToArray (array: Array<ComboboxItem>, item: any, index: number) {
  array.push(new ComboboxItem(item.metadata.title + '/' + item.metadata.from, index))
}

export function getNodeLabel (labels: any, nodeId: string) {
  if (labels !== undefined) {
    if (labels[nodeId] !== undefined) {
      return labels[nodeId]
    }
  }
  return nodeId
}

function createNode (labels: Array<Label>, nodeId: string): Node {
  return new Node(
    getNodeLabel(labels, nodeId),
    new Array<Node>(),
    new Array<Node>(),
    nodeId,
    0,
    undefined,
    undefined
  )
}

function containsNode (nodes: Array<Node>, nodeId: string) {
  let value = false
  nodes.forEach(node => {
    if (node.id === nodeId) {
      value = true
    }
  })
  return value
}

export function getNodeById (nodes: Array<Node>, id: string) {
  return nodes.filter(x => x.id === id)[0]
}

export function getNodeByKey (nodes: Array<Node>, key: number) {
  return nodes.filter(x => x.key === key)[0]
}

export function createNodes (hierarchy: any, labels: any) {
  const links: Array<Link> = mapLinks(hierarchy)
  const result = new Array<Node>()
  const visitedNodes = new Array<string>()
  links.forEach(link => {
    if (!stringArrayContainsNodeById(visitedNodes, link.child)) {
      visitedNodes.push(link.child)
      result.push(createNode(labels, link.child))
    }
    if (!stringArrayContainsNodeById(visitedNodes, link.parent)) {
      visitedNodes.push(link.parent)
      result.push(createNode(labels, link.parent))
    }
  })
  links.forEach(link => {
    const child = getNodeById(result, link.child)
    if (!containsNode(child.parents, link.parent)) {
      child.parents.push(getNodeById(result, link.parent))
    }
    const parent = getNodeById(result, link.parent)
    if (!containsNode(parent.children, link.child)) {
      parent.children.push(getNodeById(result, link.child))
    }
  })

  const NodesWithNoParent = result.filter(x => x.parents.length === 0)
  let root: Node
  if (!containsNode(result, ROOT_ID)) {
    root = createNode(labels, ROOT_ID)
  } else {
    root = getNodeById(result, ROOT_ID)
  }
  result.splice(0, 0, root)

  NodesWithNoParent.forEach(node => {
    node.parents.push(root)
    root.children.push(node)
  })
  return result
}

export function packNodes (height: number, width: number, root: Node, maxDepth: number): Array<Circle> {
  const circles = new Array<Circle>()
  const margin = 0
  const packChart = d3.pack()
  packChart.size([width - margin, height - margin])
  packChart.padding(7)
  const treeRoot = d3.hierarchy(root)
    .sum((d: any) => Math.sqrt(d.value))

  const output: any = packChart(treeRoot).descendants()
  const interpolate = function (i: number) { return d3.interpolateCool(i) }

  for (let i = 0; i < output.length; i++) {
    const color: any = interpolate(output[i].data.depth / maxDepth)
    const n: Circle = {
      key: output[i].data.key,
      fill: color,
      parent: output[i].parent !== null ? output[i].parent : null,
      id: output[i].data.id,
      label: output[i].data.label,
      isLeaf: output[i].data.isLeaf,
      x: output[i].x,
      y: output[i].y,
      r: output[i].r,
      depth: output[i].data.depth
    }
    circles.push(n)
  }
  return circles
}

export function packTreeHierarchy (root: Node, width: number, height: number) {
  const circles = Array<Circle>()
  const links = Array<Arrow>()

  const levelWidth = [1]
  const childCount = function (level: any, n: any) {
    if (n.children && n.children.length > 0) {
      if (levelWidth.length <= level + 1) {
        levelWidth.push(0)
      }
      levelWidth[level + 1] += n.children.length
      n.children.forEach(function (d: any) {
        childCount(level + 1, d)
      })
    }
  }
  childCount(0, root)

  // const treemap = d3.tree().size([height, width])
  const max: any = d3.max(levelWidth)
  const treemap = d3.tree().size([max * 45, height * 200])

  const hierarchyRoot: any = d3.hierarchy(root, function (d: any) {
    return d.children
  })
  hierarchyRoot.x0 = 0
  hierarchyRoot.y0 = width / 2

  const radius = TREE_CIRCLE_RADIUS
  const interpolate = function (i: number) { return d3.interpolateCool(i) }

  const treeData = treemap(hierarchyRoot)
  treeData.descendants().forEach((element: any) => {
    const color = interpolate(element.data.depth / height)
    const n: Circle = {
      key: element.data.key,
      fill: color,
      parent: element.parent !== null ? element.parent : null,
      id: element.data.id,
      label: element.data.label,
      isLeaf: element.data.isLeaf,
      x: element.x,
      y: element.y,
      r: radius,
      depth: element.data.depth
    }
    circles.push(n)
  })
  treeData.links().forEach((element: any, index: number) => {
    const n: Arrow = {
      id: index,
      r: 10,
      lx: element.source.x,
      ly: element.source.y,
      rx: element.target.x,
      ry: element.target.y
    }
    links.push(n)
  })
  return { circles, links }
}
