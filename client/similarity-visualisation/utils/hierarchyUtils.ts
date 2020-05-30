import { MappingNode, Node, ArrowData, ROOT_ID, Circle, Arrow, Position, Label, MappingData, MAX_TREE_DEPTH } from '../models'
import { getNodeById, getNodeLabel } from './nodesUtils'


export function createHierarchy (leftDataset: any, rightDataset: any) {
  let hierarchyArray: any = []
  if (leftDataset !== undefined) {
    hierarchyArray = hierarchyArray.concat(leftDataset.hierarchy)
  }
  if (rightDataset !== undefined) {
    hierarchyArray = hierarchyArray.concat(rightDataset.hierarchy)
  }
  return hierarchyArray
}

export function createLabels (leftDataset: any, rightDataset: any) {
  let labelsArray = {}
  if (leftDataset !== undefined) {
    labelsArray = { ...labelsArray, ...leftDataset.labels }
  }
  if (rightDataset !== undefined) {
    labelsArray = { ...labelsArray, ...rightDataset.labels }
  }
  return labelsArray
}

export function createLayer (urls: Array<MappingNode>, nodes: Array<Node>): Array<ArrowData> {
  console.log('AAA')
  console.log(urls)
  console.log(nodes)
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
  console.log(layerArray)
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
      rx: position === Position.Left ? targetNode.x - targetNode.r * 10 / 10 : targetNode.x + targetNode.r * 10 / 10,
      ry: targetNode.y,
      r: targetNode.r
    }
    counter++
    result.push(arrow)
  }
  return result
}

export function highlightTreeMapping (circles: Array<Circle>, leftMappingNodes: Array<ArrowData>, rightMappingNodes: Array<ArrowData>) {
  for (let i = 0; i < leftMappingNodes.length; i++) {
    const targetCircle = getCircleById(circles, leftMappingNodes[i].id)
    targetCircle.fill = 'red'
    targetCircle.r += 2
  }
  for (let i = 0; i < rightMappingNodes.length; i++) {
    const targetCircle = getCircleById(circles, rightMappingNodes[i].id)
    targetCircle.fill = 'red'
    targetCircle.r += 2
  }
}

function createMappingData (id: string, group: string, size: number, shared: number) {
  return new MappingData(
    id,
    group,
    shared,
    size
  )
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

// eslint-disable-next-line
export function createMapping (labels: Array<Label>, mapping: any, mappingID: number) {
  const result = Array<MappingNode>()
  const mappingDataArray = Array<MappingData>()
  mapping.mappings[mappingID].data.forEach((item: any) => {
    mappingDataArray.push(createMappingData(item.id, item.metadata.group, item.metadata.size, item.metadata.shared))
  })
  let counter = 1
  mappingDataArray.forEach(element => {
    const name = getNodeLabel(labels, element.id)
    if (result.filter(x => x.name === element.group[0]).length === 0) {
      const newChildren = createMappingNodeWithMap(counter, name, element.group[0], element.id)
      counter++
      const newNode = createMappingNodeWithChildren(counter, element.group[0], [newChildren])
      counter++
      result.push(newNode)
    } else {
      const node = result.filter(x => x.name === element.group[0])[0]
      const newChildren = createMappingNodeWithMap(counter, name, element.group[0], element.id)
      counter++
      if (node.children !== undefined) {
        node.children.push(newChildren)
      }
    }
  })
  return result
}
