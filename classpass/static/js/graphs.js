let myChart;

function renderDoughnutChart(title, labels, data) {
  const ctx = document.getElementById("chart").getContext('2d');

  // Check if a chart instance exists with the ID 'chart'
  if (myChart instanceof Chart) {
    myChart.destroy();
  }

  myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          'rgb(241, 90, 70)',
          'rgb(255, 252, 250)',
          'rgb(40, 91, 89)',
          'rgb(111, 101, 169)',
          'rgb(45, 84, 132)'
        ],
        hoverOffset: 4,
        borderColor: ['rgb(42, 42, 42)']
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: title
        }
      },
      responsive: false
    },
  });
}

function renderBarChart(title, labels, data) {
  const ctx = document.getElementById("chart").getContext('2d');

  // Check if a chart instance exists with the ID 'chart'
  if (myChart instanceof Chart) {
    myChart.destroy();
  }

  myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Data',
        data: data,
        backgroundColor: 'rgb(174,193,120)',
      }]
    },
    options: {  
      scales: {
        y: {
          ticks: {
            color: 'rgb(255, 252, 250)'
          }
        },
        x: {
          ticks: {
            color: 'rgb(255, 252, 250)'
          }
        }
      },
      color: 'rgb(255, 252, 250)',
      plugins: {
        title: {
          display: true,
          text: title,
          color: 'rgb(255, 252, 250)'
        }
      },
      responsive: false
    },
  });
}

document.addEventListener("DOMContentLoaded", async function () {
  const graphButtons = document.querySelectorAll(".btn-left");
  let graphId = 1;
  let optionsGraph;

  graphButtons.forEach(function (button) {
    button.addEventListener("click", async function () {
      graphId = button.value;

      const [typeGraph, titleGraph, labelsGraph, valuesGraph, options, defaultOption] = await graphs(graphId);
      optionsGraph = options;

      // Determine whether to show or hide the select container
      if (graphId === '4') {
        select(graphId, optionsGraph, defaultOption);
      } else {
        hideSelect();
      }

      // Determine which chart type to render
      if (typeGraph === 'doughnut') {
        renderDoughnutChart(titleGraph, labelsGraph, valuesGraph);
      } else if (typeGraph === 'bar') {
        renderBarChart(titleGraph, labelsGraph, valuesGraph);
      }
    });
  });

  // Initially load the first graph when the page is loaded
  const [typeGraph, titleGraph, labelsGraph, valuesGraph, options, defaultOption] = await graphs(graphId);
  optionsGraph = options;

  // Determine whether to show or hide the select container initially
  if (graphId === '4') {
    select(graphId, optionsGraph, defaultOption);
  } else {
    hideSelect();
  }

  // Determine which chart type to render initially
  if (typeGraph === 'doughnut') {
    renderDoughnutChart(titleGraph, labelsGraph, valuesGraph);
  } else if (typeGraph === 'bar') {
    renderBarChart(titleGraph, labelsGraph, valuesGraph);
  }

  // Add an event listener to the select element on page load
  const argsSelect = document.getElementById("argsSelect");
  argsSelect.addEventListener("change", async function () {
    const selectedValue = argsSelect.value;
    const [typeGraph, titleGraph, labelsGraph, valuesGraph] = await graphs(graphId, selectedValue);

    // Determine which chart type to render
    if (typeGraph === 'doughnut') {
      renderDoughnutChart(titleGraph, labelsGraph, valuesGraph);
    } else if (typeGraph === 'bar') {
      renderBarChart(titleGraph, labelsGraph, valuesGraph);
    }
  });

  function hideSelect() {
    document.querySelector(".select-container").style.display = "none";
  }
});

function select(id, options, defaultOption) {
  const selectContainer = document.querySelector(".select-container");
  const argsSelect = document.getElementById("argsSelect");

  // Clear existing options
  argsSelect.innerHTML = "";

  options.forEach((optionText) => {
    const option = document.createElement("option");
    option.value = optionText;
    option.textContent = optionText;

    // Check if this option should be selected
    if (optionText === defaultOption) {
      option.selected = true;
    }

    argsSelect.appendChild(option);
  });

  // Show the select container
  selectContainer.style.display = "block";
}

async function graphs(id, place, type) {
  let url = `/api/graphs/${id}`
  if (place) {
    url = url + `?place=${place}`;
  }
  if (type) {
    url = url + `?type=${type}`;
  }
  const response = await fetch(url);
  const data = await response.json();

  const typeGraph = data.type;
  const titleGraph = data.title
  const labelsGraph = data.labels.sort();
  const valuesGraph = labelsGraph.map(label => data[label]);

  let optionsGraph = null
  let defaultOption = null
  if (id === '4') {
    optionsGraph = data.options.sort();
    defaultOption = "entrance 1"
  }

  return [typeGraph, titleGraph, labelsGraph, valuesGraph, optionsGraph, defaultOption];
}
