async function getCountyData(countyId) {
  try {
    const response = await fetch('http://localhost:8000/api/counties/' + countyId + '/people');
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function displayCountyInfo(countyId) {
    const data =this.getCountyData(countyId)
        .then( response => {
            const infoDiv = document.getElementById('county-info');

            innerHtml = '';

            if (response.length > 0) {
                response.forEach(element => {
                    innerHtml += `
                        <h3>${element.name}</h3>
                        <p><strong>Position:</strong> ${element.position}</p>
                        <p><strong>Phone Number:</strong> ${element.phone}</p>
                        <p><strong>Fax Number:</strong> ${element.fax}</p>
                        <br>
                        `
                });

                innerHtml += `<button id="reset-zoom" class="reset-button">Reset Zoom</button>`

                infoDiv.innerHTML = innerHtml;
                infoDiv.style.display = 'block';

                document.getElementById('reset-zoom').addEventListener('click', resetZoom);
            } else {
                infoDiv.innerHTML = `
                    <h3>County Information</h3>
                    <p>No data available for county ${countyId}</p>
                    <button id="reset-zoom" class="reset-button">Reset Zoom</button>
                `;
                infoDiv.style.display = 'block';

                document.getElementById('reset-zoom').addEventListener('click', resetZoom);
            }
        });
}

function zoomToCounty(countyFeature) {
    const bounds = path.bounds(countyFeature);
    const dx = bounds[1][0] - bounds[0][0];
    const dy = bounds[1][1] - bounds[0][1];
    const x = (bounds[0][0] + bounds[1][0]) / 2;
    const y = (bounds[0][1] + bounds[1][1]) / 2;
    
    const scale = Math.min(8, 0.6 / Math.max(dx / width, dy / height));
    const translate = [width / 2 - scale * x, height / 2 - scale * y];
    
    svg.transition()
        .duration(750)
        .call(
            zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
        );
}

function resetZoom() {
    svg.transition()
        .duration(750)
        .call(
            zoom.transform,
            d3.zoomIdentity
        );
}

const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .on("zoom", function(event) {
        svg.selectAll("path").attr("transform", event.transform);
    });

const width = 700;
const height = 500;

const svg = d3.select("#map")
    .attr("width", width)
    .attr("height", height)
    .call(zoom);

const mapGroup = svg.append("g");

const projection = d3.geoAlbersUsa()
    .scale(1300)
    .translate([width / 2, height / 2]);

const path = d3.geoPath()
    .projection(projection);

d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json").then(function(us) {
    const states = topojson.feature(us, us.objects.states);
    const counties = topojson.feature(us, us.objects.counties);
    
    const georgia = states.features.filter(d => d.id === "13");
    const georgiaCounties = counties.features.filter(d => d.id.startsWith("13"));
    
    projection.fitSize([width, height], georgia[0]);
    
    mapGroup.selectAll(".county")
        .data(georgiaCounties)
        .enter()
        .append("path")
        .attr("class", "county")
        .attr("d", path)
        .style("cursor", "pointer")
        .on("click", function(event, d) {
            mapGroup.selectAll(".county").classed("selected", false);
            d3.select(this).classed("selected", true);
            displayCountyInfo(d.id);
            zoomToCounty(d);
        });
    
    mapGroup.selectAll(".state")
        .data(georgia)
        .enter()
        .append("path")
        .attr("class", "state")
        .attr("d", path);
}).catch(function(error) {
    console.log("Error loading map data:", error);
    
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .style("font-size", "18px")
        .style("fill", "#666")
        .text("Map data could not be loaded");
});