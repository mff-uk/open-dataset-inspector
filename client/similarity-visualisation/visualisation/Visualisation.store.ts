import { ROOT_LABEL, ROOT_ID, MAX_DEPTH, MappingNode, Labels, Node, Circle, Arrow, Position, Path, ComboboxItem, MAX_TREE_DEPTH } from '../models'
import { createTree, createLayer, getMaxTreeDepth, packMappingArrows, appendNode, createArrayFromHierarchy, highlightTreeMapping } from '../utils/hierarchyUtils'
import { packNodes, packTreeHierarchy, getNodeByKey, createVisitedNode, getNodeLabel } from '../utils/nodesUtils'
import { highlightPaths, createPathNodes } from '../utils/pathUtils'
import { VisitedNode } from '../models/VisitedNode'

export const STORE_NAME = 'Visualisation'

export const Actions = {
  RESIZE_CANVAS: 'RESIZE_CANVAS',
  CREATE_HIERARCHY_FOR_CIRCLES: 'CREATE_HIERARCHY_FOR_CIRCLES',
  CREATE_HIERARCHY_FOR_TREE: 'CREATE_HIERARCHY_FOR_TREE',
  UPDATE_CIRCLE_CANVAS: 'UPDATE_CIRCLE_CANVAS',
  UPDATE_TREE_CANVAS: 'UPDATE_TREE_CANVAS',
  ADD_NODE_TO_VISITED_NODES: 'ADD_NODE_TO_VISITED_NODES',
  UPDATE_PATH: 'UPDATE_PATH',
  SELECT_PATH: 'SELECT_PATH',
  APPEND_NODE_TREE: 'APPEND_NODE_TREE',
  CUT_NODE_TREE_CHILDREN: 'CUT_NODE_TREE_CHILDREN',
  INIT_PATH_NODES: 'INIT_PATH_NODES'
}

export const Mutations = {
  CHANGE_WINDOW: 'CHANGE_WINDOW',
  CHANGE_LEFT_MAPPING_LIST: 'CHANGE_LEFT_MAPPING_LIST',
  CHANGE_LEFT_MAPPING: 'CHANGE_LEFT_MAPPING',
  CHANGE_RIGHT_MAPPING_LIST: 'CHANGE_RIGHT_MAPPING_LIST',
  CHANGE_RIGHT_MAPPING: 'CHANGE_RIGHT_MAPPING',
  CHANGE_DEPTH: 'CHANGE_DEPTH',
  CHANGE_MAX_DEPTH: 'CHANGE_MAX_DEPTH',
  CHANGE_NODES: 'CHANGE_NODES',
  CHANGE_VISITED_NODES: 'CHANGE_VISITED_NODES',
  CHANGE_CIRCLES: 'CHANGE_CIRCLES',
  CHANGE_LEFT_ARROWS: 'CHANGE_LEFT_ARROWS',
  CHANGE_RIGHT_ARROWS: 'CHANGE_RIGHT_ARROWS',
  CHANGE_CIRCLE_HIERARCHY: 'CHANGE_CIRCLE_HIERARCHY',
  CHANGE_ROOT_ID: 'CHANGE_ROOT_ID',
  CHANGE_ACTIVE_PATH: 'CHANGE_ACTIVE_PATH',
  CHANGE_PATH_NODES: 'CHANGE_PATH_NODES',
  CHANGE_TREE_HIERARCHY: 'CHANGE_TREE_HIERARCHY',
  CHANGE_TREE_NODES: 'CHANGE_TREE_NODES',
  CHANGE_TREE_LINKS: 'CHANGE_TREE_LINKS',
  CHANGE_TREE_HEIGHT: 'CHANGE_TREE_HEIGHT',
  CHANGE_HIERARCHY: 'CHANGE_HIERARCHY'
}

export const Getters = {
  GET_TREE_HEIGHT: 'GET_TREE_HEIGHT',
  GET_LEFT_MAPPING_LIST: 'GET_LEFT_MAPPING_LIST',
  GET_LEFT_MAPPING: 'GET_LEFT_MAPPING',
  GET_RIGHT_MAPPING_LIST: 'GET_RIGHT_MAPPING_LIST',
  GET_RIGHT_MAPPING: 'GET_RIGHT_MAPPING',
  GET_DEPTH: 'GET_DEPTH',
  GET_ACTIVE_PATH: 'GET_ACTIVE_PATH',
  GET_MAX_DEPTH: 'GET_MAX_DEPTH',
  GET_NODES: 'GET_NODES',
  GET_VISITED_NODES: 'GET_VISITED_NODES',
  GET_CIRCLE_HIERARCHY: 'GET_HIERARCHY',
  GET_ROOT_ID: 'GET_ROOT_ID',
  GET_CIRCLES: 'GET_CIRCLES',
  GET_RIGHT_ARROWS: 'GET_RIGHT_ARROWS',
  GET_LEFT_ARROWS: 'GET_LEFT_ARROWS',
  GET_NODE_BY_ID: 'GET_NODE_BY_ID',
  GET_PATH_NODES: 'GET_PATH_NODES',
  GET_TREE_HIERARCHY: 'GET_TREE_HIERARCHY',
  GET_TREE_NODES: 'GET_TREE_NODES',
  GET_TREE_LINKS: 'GET_TREE_LINKS',
  GET_HIERARCHY: 'GET_HIERARCHY'
}

export default {
  namespaced: true,
  state: {
    leftMappingList: Array<ComboboxItem>(),
    leftMapping: Array<MappingNode>(),
    rightMappingList: Array<ComboboxItem>(),
    rightMapping: Array<MappingNode>(),
    nodes: Array<Node>(),
    activePath: undefined,
    pathNodes: Array<Node>(),
    circles: Array<Circle>(),
    leftArrows: Array<Arrow>(),
    rightArrows: Array<Arrow>(),
    rootId: ROOT_ID,
    hierarchy: Array<[string, string, string]>(),
    circleHierarchy: new Node(ROOT_LABEL, Array<Node>(), Array<Node>(), ROOT_ID, 0, undefined, undefined),
    treeHierarchy: new Node(ROOT_LABEL, Array<Node>(), Array<Node>(), ROOT_ID, 0, undefined, undefined),
    treeNodes: Array<Circle>(),
    treeLinks: Array<Arrow>(),
    treeHeight: 1,
    visitedNodes: Array<VisitedNode>(),
    depth: 1,
    maxDepth: MAX_DEPTH,
    window: {
      width: 0,
      height: 0
    },
    error: Error
  },
  getters: {
    [Getters.GET_MAX_DEPTH]: (state: { maxDepth: number }) => {
      return state.maxDepth
    },
    [Getters.GET_TREE_HEIGHT]: (state: { treeHeight: number }) => {
      return state.treeHeight
    },
    [Getters.GET_DEPTH]: (state: {depth: number}) => {
      return state.depth
    },
    [Getters.GET_CIRCLE_HIERARCHY]: (state: {circleHierarchy: Node}) => {
      return state.circleHierarchy
    },
    [Getters.GET_LEFT_MAPPING_LIST]: (state: {leftMappingList: Array<ComboboxItem>}) => {
      return state.leftMappingList
    },
    [Getters.GET_RIGHT_MAPPING_LIST]: (state: {rightMappingList: Array<ComboboxItem>}) => {
      return state.rightMappingList
    },
    [Getters.GET_ACTIVE_PATH]: (state: {activePath: Path}) => {
      return state.activePath
    },
    [Getters.GET_LEFT_MAPPING]: (state: {leftMapping: Array<MappingNode>}) => {
      return state.leftMapping
    },
    [Getters.GET_RIGHT_MAPPING]: (state: {rightMapping: Array<MappingNode>}) => {
      return state.rightMapping
    },
    [Getters.GET_VISITED_NODES]: (state: {visitedNodes: Array<VisitedNode>}) => {
      return state.visitedNodes
    },
    [Getters.GET_NODES]: (state: {nodes: Array<Node>}) => {
      return state.nodes
    },
    [Getters.GET_ROOT_ID]: (state: {rootId: string}) => {
      return state.rootId
    },
    [Getters.GET_CIRCLES]: (state: {circles: Circle[]}) => {
      return state.circles
    },
    [Getters.GET_RIGHT_ARROWS]: (state: {rightArrows: Arrow[]}) => {
      return state.rightArrows
    },
    [Getters.GET_LEFT_ARROWS]: (state: {leftArrows: Arrow[]}) => {
      return state.leftArrows
    },
    [Getters.GET_PATH_NODES]: (state: {pathNodes: Node[]}) => {
      return state.pathNodes
    },
    [Getters.GET_TREE_HIERARCHY]: (state: {treeHierarchy: Node}) => {
      return state.treeHierarchy
    },
    [Getters.GET_TREE_NODES]: (state: {treeNodes: Circle[]}) => {
      return state.treeNodes
    },
    [Getters.GET_TREE_LINKS]: (state: {treeLinks: Arrow[]}) => {
      return state.treeLinks
    },
    [Getters.GET_HIERARCHY]: (state: {hierarchy: Array<[string, string, string]>}) => {
      return state.hierarchy
    }
  },
  mutations: {
    [Mutations.CHANGE_ACTIVE_PATH] (state: {activePath: Path}, value: Path) {
      state.activePath = value
    },
    [Mutations.CHANGE_LEFT_MAPPING] (state: {leftMapping: Array<MappingNode>}, value: Array<MappingNode>) {
      state.leftMapping = value
    },
    [Mutations.CHANGE_RIGHT_MAPPING] (state: {rightMapping: Array<MappingNode>}, value: Array<MappingNode>) {
      state.rightMapping = value
    },
    [Mutations.CHANGE_LEFT_MAPPING_LIST] (state: {leftMappingList: Array<ComboboxItem>}, value: Array<ComboboxItem>) {
      state.leftMappingList = value
    },
    [Mutations.CHANGE_RIGHT_MAPPING_LIST] (state: {rightMappingList: Array<ComboboxItem>}, value: Array<ComboboxItem>) {
      state.rightMappingList = value
    },
    [Mutations.CHANGE_DEPTH] (state: {depth: number}, value: number) {
      state.depth = value
    },
    [Mutations.CHANGE_MAX_DEPTH] (state: {maxDepth: number}, value: number) {
      state.maxDepth = value
    },
    [Mutations.CHANGE_NODES] (state: {nodes: Array<Node>}, value: Array<Node>) {
      state.nodes = value
    },
    [Mutations.CHANGE_VISITED_NODES] (state: {visitedNodes: Array<VisitedNode>}, value: Array<VisitedNode>) {
      state.visitedNodes = value
    },
    [Mutations.CHANGE_WINDOW] (state: {window: {height: number, width: number}}, value: {width: number; height: number}) {
      state.window.height = value.height
      state.window.width = value.width
    },
    [Mutations.CHANGE_CIRCLES] (state: {circles: Array<Circle>}, value: Array<Circle>) {
      state.circles = value
    },
    [Mutations.CHANGE_LEFT_ARROWS] (state: {leftArrows: Array<Arrow>}, value: Array<Arrow>) {
      state.leftArrows = value
    },
    [Mutations.CHANGE_RIGHT_ARROWS] (state: {rightArrows: Array<Arrow>}, value: Array<Arrow>) {
      state.rightArrows = value
    },
    [Mutations.CHANGE_CIRCLE_HIERARCHY] (state: {circleHierarchy: Node}, value: Node) {
      state.circleHierarchy = value
    },
    [Mutations.CHANGE_ROOT_ID] (state: {rootId: string}, value: string) {
      state.rootId = value
    },
    [Mutations.CHANGE_PATH_NODES] (state: {pathNodes: Array<Node>}, value: Array<Node>) {
      state.pathNodes = value
    },
    [Mutations.CHANGE_TREE_HIERARCHY] (state: {treeHierarchy: Node}, value: Node) {
      state.treeHierarchy = value
    },
    [Mutations.CHANGE_TREE_NODES] (state: {treeNodes: Array<Node>}, value: Array<Node>) {
      state.treeNodes = value
    },
    [Mutations.CHANGE_TREE_HEIGHT] (state: {treeHeight: number}, value: number) {
      state.treeHeight = value
    },
    [Mutations.CHANGE_TREE_LINKS] (state: {treeLinks: Array<Arrow>}, value: Array<Arrow>) {
      state.treeLinks = value
    },
    [Mutations.CHANGE_HIERARCHY] (state: {hierarchy: Array<[string, string, string]>}, value: []) {
      state.hierarchy = value
    }
  },
  actions: {
    [Actions.CREATE_HIERARCHY_FOR_CIRCLES]: createHierarchyForCircles,
    [Actions.CREATE_HIERARCHY_FOR_TREE]: createHierarchyForTree,
    [Actions.ADD_NODE_TO_VISITED_NODES]: addNodeToVisitedNodes,
    [Actions.RESIZE_CANVAS]: resizeCanvas,
    [Actions.UPDATE_CIRCLE_CANVAS]: updateCircleCanvas,
    [Actions.UPDATE_TREE_CANVAS]: updateTreeCanvas,
    [Actions.UPDATE_PATH]: updatePath,
    [Actions.SELECT_PATH]: selectPath,
    [Actions.APPEND_NODE_TREE]: appendNodeTree,
    [Actions.CUT_NODE_TREE_CHILDREN]: cutNodeTreeChildren,
    [Actions.INIT_PATH_NODES]: initPathNodes
  }
}

function initPathNodes (context: any) {
  context.commit(Mutations.CHANGE_PATH_NODES, Array<Node>())
}

// UPRAVIT KOD
function selectPath (context: any, labels: Labels) {
  const activePath: Path = context.getters[Getters.GET_ACTIVE_PATH]
  // const nodes: Array<Node> = context.getters[Getters.GET_NODES]
  const rootId: string = activePath.vertices[activePath.up]
  const leftLabel = getNodeLabel(labels, activePath.vertices[0])
  const leftMapping: MappingNode = {
    id: 0,
    name: leftLabel
  }
  leftMapping.nodeID = activePath.vertices[0]
  leftMapping.mapBy = leftLabel
  const rightLabel = getNodeLabel(labels, activePath.vertices[activePath.vertices.length - 1])
  const rightMapping: MappingNode = {
    id: 0,
    name: rightLabel
  }
  rightMapping.nodeID = activePath.vertices[activePath.vertices.length - 1]
  rightMapping.mapBy = rightLabel
  context.commit(Mutations.CHANGE_LEFT_MAPPING, [leftMapping])
  context.commit(Mutations.CHANGE_RIGHT_MAPPING, [rightMapping])
  context.commit(Mutations.CHANGE_ROOT_ID, rootId)
  context.commit(Mutations.CHANGE_VISITED_NODES, [createVisitedNode(rootId, labels[rootId])])
  context.commit(Mutations.CHANGE_PATH_NODES, createPathNodes(context.state.nodes, context.state.activePath))
  // context.commit(Mutations.)
}

function updatePath (context: any, value: number) {
  context.commit(Mutations.CHANGE_ROOT_ID, context.state.visitedNodes[value].id)
  context.commit(Mutations.CHANGE_VISITED_NODES, context.state.visitedNodes.slice(0, value + 1))
}

function createHierarchyForCircles (context: any) {
  if (context.state.nodes.length === 0) {
    return undefined
  } else {
    if (context.state.depth === 0) {
      context.state.depth = 1
    }
    const maxDepth = getMaxTreeDepth(context.getters[Getters.GET_ROOT_ID], context.state.nodes, MAX_DEPTH)
    if (maxDepth < context.state.depth) {
      context.commit(Mutations.CHANGE_CIRCLE_HIERARCHY, createTree(context.state.rootId, context.state.nodes, maxDepth))
    } else {
      context.commit(Mutations.CHANGE_CIRCLE_HIERARCHY, createTree(context.state.rootId, context.state.nodes, context.state.depth))
    }
    if (maxDepth === 0) {
      context.commit(Mutations.CHANGE_MAX_DEPTH, 1)
      context.commit(Mutations.CHANGE_DEPTH, 1)
    } else {
      if (maxDepth < context.state.depth) {
        context.commit(Mutations.CHANGE_DEPTH, maxDepth)
      }
      context.commit(Mutations.CHANGE_MAX_DEPTH, maxDepth)
    }
  }
}

function cutNodeTreeChildren (context: any, circle: Circle) {
  if (context.state.nodes.length === 0) {
    return undefined
  } else {
    const hierarchyArray = createArrayFromHierarchy(context.state.treeHierarchy)
    const root = getNodeByKey(hierarchyArray, circle.key)
    root.children = []
    root.isLeaf = true
    context.dispatch(Actions.UPDATE_TREE_CANVAS)
  }
}

function appendNodeTree (context: any, circle: Circle) {
  if (context.state.nodes.length === 0) {
    return undefined
  } else {
    const hierarchyArray = createArrayFromHierarchy(context.state.treeHierarchy)
    const root = getNodeByKey(hierarchyArray, circle.key)
    const result = appendNode(root, context.state.nodes, hierarchyArray.length - 1, context.state.treeHeight)
    root.children = result.rootCopy.children
    root.isLeaf = false
    context.commit(Mutations.CHANGE_TREE_HEIGHT, result.maxDepth)
    context.dispatch(Actions.UPDATE_TREE_CANVAS)
  }
}

function createHierarchyForTree (context: any) {
  if (context.state.nodes.length === 0) {
    return undefined
  } else {
    context.commit(Mutations.CHANGE_TREE_HIERARCHY, createTree(context.state.rootId, context.state.nodes, MAX_TREE_DEPTH))
    context.commit(Mutations.CHANGE_TREE_HEIGHT, MAX_TREE_DEPTH)
  }
}

function resizeCanvas (context: any, value: {width: number; height: number}) {
  context.commit(Mutations.CHANGE_WINDOW, value)
}

function createCircles (context: any): Array<Circle> {
  return packNodes(context.state.window.height, context.state.window.width, context.state.circleHierarchy, context.state.maxDepth)
}

function updateCircleCanvas (context: any) {
  context.commit(Mutations.CHANGE_CIRCLES, createCircles(context))
  context.commit(Mutations.CHANGE_LEFT_ARROWS, packMappingArrows(context.state.window.height, context.state.window.width,
    context.state.circles, createLayer(context.state.leftMapping, context.state.nodes), Position.Left))
  context.commit(Mutations.CHANGE_RIGHT_ARROWS, packMappingArrows(context.state.window.height, context.state.window.width,
    context.state.circles, createLayer(context.getters[Getters.GET_RIGHT_MAPPING], context.state.nodes), Position.Right))
  if (context.state.activePath !== undefined) {
    context.commit(Mutations.CHANGE_CIRCLES, highlightPaths(context.state.circles, context.state.activePath))
  }
}

function updateTreeCanvas (context: any) {
  const result = packTreeHierarchy(context.state.treeHierarchy, context.state.window.width, context.state.treeHeight)
  context.commit(Mutations.CHANGE_TREE_NODES, result.circles)
  context.commit(Mutations.CHANGE_TREE_LINKS, result.links)
  highlightTreeMapping(context.state.treeNodes,
    createLayer(context.getters[Getters.GET_LEFT_MAPPING], context.state.nodes),
    createLayer(context.getters[Getters.GET_RIGHT_MAPPING], context.state.nodes))
  if (context.state.activePath !== undefined) {
    context.commit(Mutations.CHANGE_TREE_NODES, highlightPaths(context.state.treeNodes, context.state.activePath))
  }
}

function addNodeToVisitedNodes (context: any, data: { labels: Labels; leaf: Circle }) {
  context.commit(Mutations.CHANGE_ROOT_ID, data.leaf.id)
  const array = Array<VisitedNode>()
  array.push({
    id: data.leaf.id,
    label: getNodeLabel(data.labels, data.leaf.id)
  })
  let parent = data.leaf.parent
  while (parent !== null) {
    if (parent.data.id !== ROOT_ID && parent.parent != null) {
      array.push({
        id: parent.data.id,
        label: getNodeLabel(data.labels, parent.data.id)
      })
    }
    parent = parent.parent
  }
  while (array.length !== 0) {
    const element = array.pop()
    if (element !== undefined) {
      context.state.visitedNodes.push(element)
    }
  }
}
