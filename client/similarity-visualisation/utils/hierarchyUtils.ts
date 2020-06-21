import { MappingNode, Node, ArrowData, ROOT_ID, Circle, Arrow, Position, Labels, MAX_TREE_DEPTH } from '../models'
import { getNodeById, getNodeLabel } from './nodesUtils'

export function createHierarchy (leftDataset: {hierarchy: [string, string, string]}, rightDataset: {hierarchy: [string, string, string]}) {
  let hierarchyArray: any = []
  if (leftDataset !== undefined) {
    hierarchyArray = hierarchyArray.concat(leftDataset.hierarchy)
  }
  if (rightDataset !== undefined) {
    hierarchyArray = hierarchyArray.concat(rightDataset.hierarchy)
  }
  return hierarchyArray
}

export function createLabels (leftDataset: {labels: Labels}, rightDataset: {labels: Labels}) {
  let labelsArray: Labels = {}
  if (leftDataset !== undefined) {
    labelsArray = { ...labelsArray, ...leftDataset.labels }
  }
  if (rightDataset !== undefined) {
    labelsArray = { ...labelsArray, ...rightDataset.labels }
  }
  return labelsArray
}

export function createLayer (urls: Array<MappingNode>, nodes: Array<Node>): Array<ArrowData> {
  const layerArray = Array<ArrowData>()
  for (let i = 0; i < urls.length; i++) {
    const n = nodes.filter(y => y.id === urls[i].nodeID)[0]
    if (n === undefined) {
      continue
    }
    const stack = Array<Node>()
    stack.push(n)
    const visitedArray = Array<string>()
    while (stack.length !== 0) {
      const parent = stack.pop()
      if (parent !== undefined) {
        if (parent.id === ROOT_ID) {
          continue
        }
        if (parent.parents === null) {
          continue
        }
        if (parent.depth == null) {
          if (parent.parents != null) {
            for (let i = 0; i < parent.parents.length; i++) {
              if (!visitedArray.includes(parent.parents[i].id)) {
                visitedArray.push(parent.parents[i].id)
                stack.push(parent.parents[i])
              }
            }
          }
        } else {
          if (layerArray.filter(p => p.id === parent.id).length === 0) {
            const n: ArrowData = {
              id: parent.id,
              label: urls[i].name,
              word: urls[i].mapBy
            }
            layerArray.push(n)
          }
        }
      }
    }
  }
  return layerArray
}

export function createArrayFromHierarchy (root: Node) {
  const queue = Array<Node>()
  const result = Array<Node>()
  queue.push(root)
  while (queue.length !== 0) {
    const vertex = queue.shift()
    if (vertex !== undefined) {
      result.push(vertex)
      if (vertex.children !== undefined && vertex.children !== null) {
        for (let i = 0; i < vertex.children.length; i++) {
          queue.push(vertex.children[i])
        }
      }
    }
  }
  return result
}

export function createArrows (root: Node, position: Position, ids: Array<MappingNode>, nodes: Array<Node>): void {
  if (ids !== null && ids !== undefined) {
    packMappingArrows(1000, 1000, Array<Circle>(), createLayer(ids, nodes), position)
  }
}

function copyNode (node: Node) {
  return new Node(
    node.label,
    node.parents,
    Array<Node>(),
    node.id,
    node.key,
    node.depth,
    node.color
  )
}

function resetNodeDepths (nodes: Array<Node>) {
  nodes.forEach(element => {
    element.depth = undefined
  })
}

function setNodeAsLeaf (node: Node) {
  node.children = []
  node.value = 1
  node.isLeaf = true
}

export function collapseIrrelevantSubtrees (root: Node, vertices: string[]) {
  const queue = Array<Node>()
  queue.push(root)
  while (queue.length !== 0) {
    const vertex = queue.shift()
    if (vertex !== undefined) {
      if (vertices.includes(vertex.id)) {
        if (vertex.children !== undefined && vertex.children !== null) {
          for (let i = 0; i < vertex.children.length; i++) {
            queue.push(vertex.children[i])
          }
        }
      } else {
        setNodeAsLeaf(vertex)
      }
    }
  }
  return root
}

export function createTree (rootId: string, nodes: Array<Node>, depth: number) {
  resetNodeDepths(nodes)
  const root = getNodeById(nodes, rootId)
  const rootCopy = copyNode(root)
  let keyCounter = 0
  rootCopy.key = keyCounter
  keyCounter++
  root.depth = 0
  rootCopy.depth = 0
  let maxDepth = 0
  const queue = [rootCopy]
  while (queue.length !== 0) {
    const node = queue.shift()
    if (node === undefined) { continue }
    const children = getNodeById(nodes, node.id).children
    if (children === undefined) { continue }
    if (children.length === 0) {
      setNodeAsLeaf(node)
    } else {
      children.forEach(child => {
        const childCopy = copyNode(child)
        childCopy.key = keyCounter
        keyCounter++
        node.children.push(childCopy)
        if (node.depth !== undefined) {
          const childDepth = node.depth + 1
          childCopy.depth = childDepth
          child.depth = childDepth
          if (maxDepth < childDepth) {
            maxDepth = childDepth
          }
          if (childDepth < depth) {
            queue.push(childCopy)
          } else {
            if (childDepth === depth) {
              setNodeAsLeaf(childCopy)
            }
          }
        }
      })
    }
  }
  return rootCopy
}

export function appendNode (root: Node, nodes: Array<Node>, maxKey: number, treeHeight: number) {
  resetNodeDepths(nodes)
  const rootCopy = copyNode(root)
  let keyCounter = maxKey
  rootCopy.key = keyCounter
  keyCounter++
  rootCopy.depth = root.depth
  const depth = root.depth !== undefined ? root.depth + MAX_TREE_DEPTH : MAX_TREE_DEPTH
  let maxDepth = treeHeight
  const queue = [rootCopy]
  while (queue.length !== 0) {
    const node = queue.shift()
    if (node === undefined) { continue }
    const children = getNodeById(nodes, node.id).children
    if (children === undefined) { continue }
    if (children.length === 0) {
      setNodeAsLeaf(node)
    } else {
      children.forEach(child => {
        const childCopy = copyNode(child)
        childCopy.key = keyCounter
        keyCounter++
        node.children.push(childCopy)
        if (node.depth !== undefined) {
          const childDepth = node.depth + 1
          childCopy.depth = childDepth
          child.depth = childDepth
          if (maxDepth < childDepth) {
            maxDepth = childDepth
          }
          if (childDepth < depth) {
            queue.push(childCopy)
          } else {
            if (childDepth === depth) {
              setNodeAsLeaf(childCopy)
            }
          }
        }
      })
    }
  }

  return { rootCopy, maxDepth }
}

export function getMaxTreeDepth (rootId: string, nodes: Array<Node>, depth: number) {
  resetNodeDepths(nodes)
  const root = getNodeById(nodes, rootId)
  const rootCopy = copyNode(root)
  root.depth = 0
  rootCopy.depth = 0
  let maxDepth = 0
  const queue = [rootCopy]
  while (queue.length !== 0) {
    const node = queue.shift()
    if (node === undefined) { continue }
    const children = getNodeById(nodes, node.id).children
    if (children === undefined) { continue }
    if (children.length === 0) {
      setNodeAsLeaf(node)
    } else {
      children.forEach(child => {
        const childCopy = copyNode(child)
        node.children.push(childCopy)
        if (node.depth !== undefined) {
          const childDepth = node.depth + 1
          childCopy.depth = childDepth
          child.depth = childDepth
          if (maxDepth < childDepth) {
            maxDepth = childDepth
          }
          if (childDepth < depth) {
            queue.push(childCopy)
          } else {
            if (childDepth === depth) {
              setNodeAsLeaf(childCopy)
            }
          }
        }
      })
    }
  }
  return maxDepth
}

function getCircleById (circles: Array<Circle>, id: string) {
  return circles.filter(x => x.id === id)[0]
}

export function packMappingArrows (height: number, width: number, circles: Array<Circle>, viewDepthLevel: Array<ArrowData>, position: Position): Array<Arrow> {
  let counter = 0
  const result = new Array<Arrow>()
  for (let i = 0; i < viewDepthLevel.length; i++) {
    const targetNode = getCircleById(circles, viewDepthLevel[i].id)
    const arrow: Arrow = {
      id: counter,
      word: viewDepthLevel[i].word,
      mapTo: viewDepthLevel[i].label,
      lx: position === Position.Left ? 0 : width,
      ly: height / 2,
      rx: position === Position.Left ? targetNode.x - targetNode.r : targetNode.x + targetNode.r,
      ry: targetNode.y,
      r: targetNode.r
    }
    counter++
    result.push(arrow)
  }
  return result
}

function mappingsIntersection (leftMappingNodes: Array<ArrowData>, rightMappingNodes: Array<ArrowData>) {
  return leftMappingNodes.filter(n => rightMappingNodes.some(n2 => n.id == n2.id))
}

export function highlightTreeMapping (circles: Array<Circle>, leftMappingNodes: Array<ArrowData>, rightMappingNodes: Array<ArrowData>) {

  const intersection = mappingsIntersection(leftMappingNodes, rightMappingNodes)
  for (let i = 0; i < leftMappingNodes.length; i++) {
    const targetCircle = getCircleById(circles, leftMappingNodes[i].id)
    if (targetCircle !== undefined) {
      targetCircle.fill = 'red'
    }
  }
  for (let i = 0; i < rightMappingNodes.length; i++) {
    const targetCircle = getCircleById(circles, rightMappingNodes[i].id)
    if (targetCircle !== undefined) {
      targetCircle.fill = 'blue'
    }
  }

  for (let i = 0; i < intersection.length; i++) {
    const targetCircle = getCircleById(circles, intersection[i].id)
    if (targetCircle !== undefined) {
      targetCircle.fill = 'blue'
      targetCircle.strokewidth = '7'
      targetCircle.stroke = 'red'
    }
  }
}

function createMappingNodeWithChildren (id: number, name: string, children: MappingNode[]) {
  const newNode: MappingNode = {
    id: id,
    name: name,
    children: children
  }
  return newNode
}

function createMappingNodeWithMap (id: number, name: string, mapBy: string, nodeID: string) {
  const newNode: MappingNode = {
    id: id,
    name: name,
    mapBy: mapBy,
    nodeID: nodeID
  }
  return newNode
}

export function createPathLabels (mapping: any) {
  const mapArray: {[key: string]: string[]} = {}
  let datas: any = []
  mapping.mappings.forEach((element: any) => {
    datas = datas.concat(element.data)
  });
  datas.forEach((item: any) => {
    item.metadata.group.forEach((element: string) => {
      if (mapArray[item.id] === undefined) {
        mapArray[item.id] = Array<string>()
      }
      mapArray[item.id].push(element)
    });
  })
  return mapArray
}

// eslint-disable-next-line
export function createMapping (labels: Labels, mapping: any, mappingID: number) {
  const result = Array<MappingNode>()
  const mapArray: {[key: string]: string[]} = {}
  let datas: any = []
  if (mappingID >= mapping.mappings.length) {
    mapping.mappings.forEach((element: any) => {
      datas = datas.concat(element.data)
    });
  } else {
    datas = mapping.mappings[mappingID].data
  }

  datas.forEach((item: any) => {
    const name: string = item.id
    item.metadata.group.forEach((element: string) => {
      if (mapArray[element] === undefined) {
        mapArray[element] = Array<string>()
      }
      if (!mapArray[element].includes(name)) {
        mapArray[element].push(name)
      }
    });
  })
  let counter = 0
  for (const item in mapArray) {
    const nodes = mapArray[item]
    const mappingNodes: Array<MappingNode> = []
    const rootName = getNodeLabel(labels, item)
    nodes.forEach((element: string) => {
      const name = getNodeLabel(labels, element)
      mappingNodes.push(createMappingNodeWithMap(counter++, name, item, element))
    })
    result.push(createMappingNodeWithChildren(counter++, item, mappingNodes))
  }
  return result
}

export function chooseItemFromMapping (mapping: Array<MappingNode>, id: string) {
  let result: number[] = []
  let childrens: Array<MappingNode> = []
  mapping.forEach((item: MappingNode) => {
    item.children?.forEach((children: MappingNode) => {
      childrens.push(children)
    })
  })
  childrens.forEach((children: MappingNode) => {
    if (children.nodeID === id) {
      result.push(children.id)
    }
  })
  return result
}

