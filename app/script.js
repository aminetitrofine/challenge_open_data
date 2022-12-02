const width = 700, height = 490;
const path = d3.geoPath();
const startYear = 2016;

const projection = d3.geoConicConformal()
    .center([2.454071, 46.279229])
    .scale(2600)
    .translate([width / 2, height / 2]);

path.projection(projection);
 
const svg = d3.select('#map').append("svg")
    .attr("id", "svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class","map");

const deps = svg.append("g");
const circles = d3.select('#svg').append("g");

var promises = [] ;
promises.push(d3.json('https://france-geojson.gregoiredavid.fr/repo/departements.geojson'));
promises.push(d3.json('https://raw.githubusercontent.com/aminetitrofine/open-data/main/Result.json'));
promises.push(d3.json('https://raw.githubusercontent.com/aminetitrofine/open-data/main/Result_nitrate.json'));
Promise.all(promises).then(function(values) {
    const geojson = values[0]; 
    const json_data = values[1]; 
    const data_nitrate = values[2];
    
    const quantile_circles =(number) =>{
        if(number<25){
            return 0;
        }
        else if(number<40){
            return 1;
        }
        else if(number<50){
            return 2;
        }
        else{
            return 3;
        }
    }

    

    
    var features = deps
        .selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
        .attr('id', d=> "d"+ d.properties.code)
        .attr("d", path);

    
    var drawMap = (confirmType,year,month)=>{
        var colorScale_circles = d3.scaleQuantize()
        .domain([0,4])
        .range(["#ADD8E6","yellow","orange","red"]);

        const svg_circle = circles.selectAll('circle')
            .data(data_nitrate["eau_souterraines"])
            .enter()
            .append("circle")
            .attr("cx",d=> projection([d["Longitude"],d["Latitude"]])[0])
            .attr("cy", d=>projection([d["Longitude"],d["Latitude"]])[1])
            .attr("r", 1.5)
            .style("fill", d=>colorScale_circles(quantile_circles(d["ND_AvgAnnValue"])))


        d3.select("#legend_circle").remove();
        var legend_circle = svg.append('g')
            .attr('transform', 'translate(100, 480)')
            .attr('id', 'legend_circle');
        
        legend_circle.selectAll('.colorbar')
            .data(d3.range(4))
            .enter()
            .append('svg:circle')
            .attr('cy', '0px')
            .attr('cx', d=> d* 150 + 'px')
            .attr("r",5)
            .attr("fill",d=>colorScale_circles(d))

        d3.select("#legendScale_circle").remove();
        var legendScale_circle = svg.append('g')
            .attr('transform', 'translate(110, 485)')
            .attr('id', 'legendScale_circle');
        
        const colorValues = ["NO3 moins de 25","25 à moins de 40","40 à moins de 50","50 ou plus"]
        legendScale_circle.selectAll('.textColor')
            .data(colorValues)
            .enter()
            .append('svg:text')
            .attr('y', '0px')
            .attr('x', d=> colorValues.indexOf(d)* 150 + 'px')
            .text(d=>d)


        const data = json_data[year-startYear][year][month]['departs'];
            // variation de 9 cols entre 0 et max
        var quantile = d3.scaleQuantile()
            .domain([50, 100])
            .range(d3.range(9));

        var colorScale = d3.scaleQuantize()
            .domain([0,9])
            .range(colorbrewer.Greens[9]);
        
        d3.select("#legend").remove();
        var legend = svg.append('g')
            .attr('transform', 'translate(560, 150)')
            .attr('id', 'legend');
        
        legend.selectAll('.colorbar')
            .data(d3.range(9))
            .enter().append('svg:rect')
                .attr('y', d => d * 20 + 'px')
                .attr('height', '20px')
                .attr('width', '20px')
                .attr('x', '0px')
                .attr("class", d => "q" + d + "-9")
                .attr("fill",d=>colorScale(d))

        var legendScale = d3.scaleLinear()
            .domain([50, 100])
            .range([0, 9 * 20]);

        d3.select("#legendAxis").remove();
        var legendAxis = svg.append("g")
            .attr('transform', 'translate(600, 150)')
            .attr('id','legendAxis')
            .call(d3.axisRight(legendScale).ticks(6));


        data.forEach(function(e,i) {
            d3.select("#d" + e['cddept'].substring(1,3))
                .attr("fill",colorScale(quantile(+e[confirmType])))
                .on("mouseover", function(event, d) {
                    div.transition()        
                        .duration(200)      
                        .style("opacity", .9);
                    div.html("Code : " + d.properties.code + "<br/>"
                        + "Région : " + d.properties.nom + "<br/>"
                        + "conformité bactériologique : " + e[confirmType] + "<br/>")
                        .style("left", (event.pageX + 30) + "px")     
                        .style("top", (event.pageY - 30) + "px");
        
                })
                .on("mouseout", function(event, d) {
                        div.style("opacity", 0);
                        div.html("")
                            .style("left", "-500px")
                            .style("top", "-500px");
                });
            });
            d3.select("select").on("change", function() {
                d3.selectAll("svg").attr("class", this.value);
            });
        
    }

    var drawStackedBar = (year,month) => {
        const data = json_data[year-startYear][year][month]['nature_eau_conf_bacterio'];

        // set the dimensions and margins of the graph
        const marginStackedCharts = {top: 80, right: 30, bottom: 20, left: 50},
        widthStackedCharts = 460 - marginStackedCharts.left - marginStackedCharts.right,
        heightStackedCharts = 450 - marginStackedCharts.top - marginStackedCharts.bottom;

        // append the svg object to the body of the page
        d3.select("#chart").remove();
        const svgStackedCharts = d3.select("#stackedBarChart")
            .append("svg")
            .attr("width", widthStackedCharts + marginStackedCharts.left + marginStackedCharts.right)
            .attr("height", heightStackedCharts + marginStackedCharts.top + marginStackedCharts.bottom)
            .attr("id","chart")
            .append("g")
            .attr("transform", `translate(${marginStackedCharts.left},${marginStackedCharts.top})`);
            
        // List of subgroups = header of the csv files = soil condition here
        const subgroups = ["ESO","EMI","ESU","MER"]

        // List of groups = species here = value of the first column called group -> I show them on the X axis
        const groups = data.map(d => (d["domaineparconf"]))
    
        d3.select("#legend_bar_svg").remove();
        var legend = d3.select("#stackedBarChart")
            .append("svg")
            .attr("width",60)
            .attr("height",120)
            .attr("id","legend_bar_svg")
            .attr('transform', 'translate(0,-130)')
            .append('g')
            .attr('id', 'legend_bar');

        const colorList=['#7d5736','#3a9063','#347cb6','#00335e']
        legend.selectAll('.colorbar')
            .data(d3.range(4))
            .enter().append('svg:rect')
                .attr('y', d => d * 25 + 'px')
                .attr('height', '25')
                .attr('width', '25px')
                .attr('x', '0px')
                .attr("fill",d=>colorList[d])

        var legendScale = d3.scaleBand()
            .domain(subgroups)
            .range([0,100]);
    
      
        var legendAxis = d3.selectAll("#legend_bar_svg")
            .append("g")
            .attr('transform', 'translate(30,0)')
            .attr('id','legendAxis_bar')
            .call(d3.axisRight(legendScale).ticks(4));

        // Add X axis
        const x = d3.scaleBand()
            .domain(groups)
            .range([0, widthStackedCharts])
            .padding([0.2])

        svgStackedCharts.append("g")
            .attr("transform", `translate(0, ${heightStackedCharts})`)
            .call(d3.axisBottom(x).tickSizeOuter(0));

        // Add Y axis
        
        const y = d3.scaleLinear()
            .domain([0, 100])
            .range([ heightStackedCharts, 0 ]);

        svgStackedCharts.append("g")
            .call(d3.axisLeft(y));

        // color palette = one color per subgroup
        const color = d3.scaleOrdinal()
            .domain(subgroups)
            .range(['#7d5736','#3a9063','#347cb6','#00335e'])

        //stack the data? --> stack per subgroup
        const stackedData = d3.stack()
            .keys(subgroups)(data)

        // Show the bars
        svgStackedCharts.append("g")
            .selectAll("g")
            // Enter in the stack data = loop key per key = group per group
            .data(stackedData)
            .join("g")
            .attr("fill", d => color(d.key))
            .selectAll("rect")
            // enter a second time = loop subgroup per subgroup to add all rectangles
                .data(d => d)
                .join("rect")
                    .attr("x", d => x(d.data.domaineparconf))
                    .attr("y", d => y(d[1]))
                    .attr("height", d => y(d[0]) - y(d[1]))
                    .attr("width",x.bandwidth())
    }

    let confirmType="conformbacterio";
    let year = startYear;
    let month = 0;
    drawMap(confirmType,year,month);
    d3.selectAll("input[name='conformitySelector']").on("change", function(e){
        confirmType = e.currentTarget.value;
        drawMap(confirmType,year,month);
    });

    d3.selectAll("#dateslider").on("change", function(e){
        year = startYear + Math.floor(e.currentTarget.value/12)
        month = e.currentTarget.value%12;
        drawMap(confirmType,year,month);
        drawStackedBar(year,month);
    });
    drawStackedBar(year,month);


});


let div = d3.select("body").append("div")
    .attr("class", "map-tooltip")
    .style("opacity", 0);

//bar----chart






