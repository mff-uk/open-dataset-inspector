<template>
  <div style="height: 100%">
    <svg />
    <v-overlay :value="computingPositions">
      Computing position ... <br> <br>
      <v-progress-circular
        :rotate="-90"
        :size="100"
        :width="15"
        :value="computingProgress"
        color="primary"
      >
        {{ computingProgress }}
      </v-progress-circular>
    </v-overlay>
    <div
      class="tooltip"
      style="position: absolute; opacity: 0.0; top: 0;"
    >
      <span v-show="selected.directlyMapped">
        Directly mapped
      </span>
      <span v-show="!selected.directlyMapped">
        Reduced
      </span>
      <br>
      ID:{{ selected.id }} <br>
      Label: {{ selected.label }} <br>
      Tokens: {{ selected.mappedBy }}
    </div>
    <div style="position: absolute; top: -10rem;">
      <input
        id="copy-to-clipboard"
        type="text"
      >
    </div>
  </div>
</template>

<script>
/* eslint-disable no-param-reassign */

import * as d3 from "d3";

export default {
  "name": "d3-chart-network",
  "data": () => ({
    "selected": {
      "id": "",
      "label": "",
      "directlyMapped": false,
      "node": undefined,
      "mappedBy": "",
    },
    "computingPositions": false,
    "computingProgress": 0,
  }),
  "props": {
    "nodes": Array,
    "edges": Array,
    "highlight": Object,
    "labels": Object,
    "nodesProperties": Object,
  },
  "mounted": function () {
    initializeD3Svg(this, this.$el);
    // Initial calls.
    this.updateNetwork();
    this.updateColors();
  },
  "watch": {
    "nodes": function () {
      this.updateNetwork();
    },
    "edges": function () {
      this.updateNetwork();
    },
    "highlight": function () {
      this.updateColors();
    },
  },
  "methods": {
    "updateNetwork": function () {
      updateNetwork(
        this.$local.svg,
        this.$local.simulation,
        this.edges,
        this.nodes,
        this.highlight,
        this.$local.actions,
        this.setComputingPositions
      );
      updateColors(this.$local.svg, this.nodes, this.highlight);
    },
    "updateColors": function () {
      updateColors(this.$local.svg, this.nodes, this.highlight);
    },
    "setComputingPositions": function (status, value) {
      this.computingPositions = status;
      this.computingProgress = value;
    },
  },
};

function initializeD3Svg($this, element) {
  const svg = d3.select(element).select("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .call(d3.zoom().on("zoom", () => {
      svg.attr("transform", d3.event.transform);
    }))
    .append("g");

  svg.append("g").attr("class", "lines");
  svg.append("g").attr("class", "nodes");

  const tooltip = d3.select(element).select("div.tooltip");

  const bounding = element.getBoundingClientRect();
  const center = d3.forceCenter(bounding.width / 2, bounding.height / 2);
  const simulation = d3.forceSimulation(null)
    .force("charge", d3.forceManyBody())
    .force("center", center);

  $this.$local = {
    "svg": svg,
    "tooltip": tooltip,
    "actions": {},
    "simulation": simulation,
  };

  $this.$local.actions.onMouseOver = (item) => {
    $this.$local.tooltip
      .style("left", `${d3.event.layerX}px`)
      .style("top", `${d3.event.layerY}px`);
    $this.$local.tooltip
      .transition()
      .duration(200)
      .style("opacity", 0.9);
    const nodeProperties = $this.nodesProperties[item.id];
    $this.selected = {
      "id": item.id,
      "label": $this.labels[item.id],
      "node": nodeProperties,
      "mappedBy": "",
    };
    if (nodeProperties !== undefined) {
      $this.selected.directlyMapped = nodeProperties.directlyMapped;
      if (nodeProperties.mappedBy.size > 0) {
        const mappedByStr = Array.from(nodeProperties.mappedBy).join("', '");
        $this.selected.mappedBy = `'${mappedByStr}'`;
      }
    }
  };

  $this.$local.actions.onMouseOut = () => {
    $this.$local.tooltip
      .transition()
      .duration(500)
      .style("opacity", 0);
  };
}

function updateNetwork(
  svg, simulation, edges, nodes, highlight, actions, setComputing
) {
  const linkElements = svg
    .select("g.lines")
    .selectAll("line")
    .data(edges);
  linkElements.exit().remove();
  linkElements.enter()
    .append("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6);

  const nodeElements = svg
    .select("g.nodes")
    .selectAll("circle")
    .data(nodes);
  nodeElements.exit().remove();
  nodeElements.enter()
    .append("circle")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .attr("r", 10)
    .on("mouseover", actions.onMouseOver)
    .on("mouseout", actions.onMouseOut);

  updatePositions(svg, simulation, nodes, edges, setComputing);
}

function updatePositions(svg, simulation, nodes, edges, setComputing) {
  const linkElements = svg
    .select("g.lines")
    .selectAll("line")
    .data(edges);

  const nodeElements = svg
    .select("g.nodes")
    .selectAll("circle")
    .data(nodes);

  const START_ALPHA = 1.0;
  const UPDATE_ALPHA = 0.05;

  simulation.stop();

  simulation
    .nodes(nodes)
    .force("link", d3.forceLink(edges).id((item) => item.id))
    .alpha(START_ALPHA);

  simulation.restart();

  simulation.on("tick", () => {
    if (simulation.alpha() > UPDATE_ALPHA) {
      const value = Math.floor((1 - simulation.alpha()) * 100);
      setComputing(true, value);
      return;
    }

    linkElements
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    nodeElements
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y);

    setComputing(false);
  });
  setComputing(true, 0);

  nodeElements.call(addDragSupport(simulation));
}

function updateColors(svg, nodes, highlight) {
  svg
    .selectAll("circle")
    .data(nodes)
    .attr("fill", (node) => selectColor(node, highlight));
  // TODO Multicolor?
  // https://www.d3-graph-gallery.com/graph/pie_basic.html
}

function selectColor(node, highlight) {
  let finalColor = null;
  Object.keys(highlight).forEach((color) => {
    if (highlight[color].has(node.id)) {
      if (finalColor == null) {
        finalColor = color;
      } else {
        finalColor = "yellow";
      }
    }
  });
  if (finalColor === null) {
    return "grey";
  }
  return finalColor;
}

function addDragSupport(simulation) {
  function dragStarted(item) {
    if (!d3.event.active) {
      simulation
        .alphaTarget(0.01)
        .restart();
    }
    item.fx = item.x;
    item.fy = item.y;
    copyToClipboard(item.id);
  }

  function dragged(item) {
    item.fx = d3.event.x;
    item.fy = d3.event.y;
  }

  function dragEnded(item) {
    if (!d3.event.active) {
      simulation.alphaTarget(0.0);
    }
    item.fx = null;
    item.fy = null;
  }

  return d3.drag()
    .on("start", dragStarted)
    .on("drag", dragged)
    .on("end", dragEnded);
}

/**
 * Need element in the  DOM.
 */
function copyToClipboard(value) {
  const copyText = document.getElementById("copy-to-clipboard");
  copyText.value = `https://www.wikidata.org/wiki/${value}`;
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile.
  document.execCommand("copy");
}

</script>

<style>
  .tooltip {
    position: absolute;
    text-align: left;
    padding: 0.5rem;
    background: lightsteelblue;
    border: 0;
    border-radius: 8px;
    pointer-events: none;
  }
</style>
