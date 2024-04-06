

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("show-chart");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
clearChart('chart-container');
modal.style.display = "none";

}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
if (event.target == modal) {
  modal.style.display = "none";
}
}

function createChart(num1, num2) {
  const data = [
    { label: 'Voted', value: num1 },
    { label: 'Not Voted', value: num2 - num1 },
  ];

  const svg = d3.select('#chart-container')
    .append('svg')
    .attr('width', 300)
    .attr('height', 300);

  const width = svg.attr('width');
  const height = svg.attr('height');
  const radius = Math.min(width, height) / 2;
  const g = svg.append('g').attr('transform', `translate(${width / 2}, ${height / 2})`);

  const color = d3.scaleOrdinal(['#FF6384', '#36A2EB']);

  const pie = d3.pie().value(d => d.value);

  const path = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

  const arc = g.selectAll('arc')
    .data(pie(data))
    .enter()
    .append('g')
    .attr('class', 'arc');

  arc.append('path')
    .attr('d', path)
    .attr('fill', d => color(d.data.label));

  arc.append('text')
    .attr('transform', d => `translate(${path.centroid(d)})`)
    .attr('dy', '0.35em')
    .text(d => `${d.data.label}: ${(d.data.value / num2 * 100).toFixed(1)}%`);
}


const button = document.getElementById('show-chart');
const dataElement = document.getElementById('data');
const num1 = dataElement.getAttribute('data-num1');
const num2 = dataElement.getAttribute('data-num2');

button.addEventListener('click', () => {
createChart(num1, num2);
});
function clearChart(elementId) {
d3.select(`#${elementId} svg`).remove();
}


function logout() {
    window.location.href = "/logout";
  }