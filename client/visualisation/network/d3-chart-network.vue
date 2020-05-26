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
      ID:{{ selected.id }} <br>
      Label: {{ selected.label }}
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
    },
    "computingPositions": false,
    "computingProgress": 0,
  }),
  "props": {
    "nodes": Array,
    "edges": Array,
    "highlight": Object,
    "labels": Object,
  },
  "mounted": function () {
    const svg = d3.select(this.$el).select("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .call(d3.zoom().on("zoom", () => {
        svg.attr("transform", d3.event.transform);
      }))
      .append("g");

    const tooltip = d3.select(this.$el).select("div.tooltip");

    const bounding = this.$el.getBoundingClientRect();
    const center = d3.forceCenter(bounding.width / 2, bounding.height / 2);
    const simulation = d3.forceSimulation(null)
      .force("charge", d3.forceManyBody())
      .force("center", center);

    this.$local = {
      "svg": svg,
      "tooltip": tooltip,
      "actions": {},
      "simulation": simulation,
    };

    const $this = this;

    this.$local.actions.onMouseOver = (item) => {
      $this.$local.tooltip
        .style("left", `${d3.event.layerX}px`)
        .style("top", `${d3.event.layerY}px`);
      $this.$local.tooltip
        .transition()
        .duration(200)
        .style("opacity", 0.9);
      $this.selected = {
        "id": item.id,
        "label": this.labels[item.id],
      };
    };

    this.$local.actions.onMouseOut = () => {
      $this.$local.tooltip
        .transition()
        .duration(500)
        .style("opacity", 0);
    };
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

function updateNetwork(
  svg, simulation, edges, nodes, highlight, actions, setComputing
) {
  const linkElements = svg
    .selectAll("line")
    .data(edges);

  linkElements.enter()
    .append("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6);
  const nodeElements = svg
    .selectAll("circle")
    .data(nodes);

  nodeElements.enter()
    .append("circle")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .attr("r", 10)
    .on("mouseover", actions.onMouseOver)
    .on("mouseout", actions.onMouseOut);

  updatePositions(
    simulation, nodes, edges, linkElements, nodeElements, setComputing
  );
}

function updatePositions(
  simulation, nodes, edges, linkElements, nodeElements, setComputing
) {
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
  // TODO Multicolor
  // https://www.d3-graph-gallery.com/graph/pie_basic.html
  // gradient
}

function selectColor(node, highlight) {
  // TODO We can return all available colors.
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
