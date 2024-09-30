// 定义 zoomed 函数，用于处理缩放事件
function zoomed(event) {
    svg.selectAll("circle").attr("transform", event.transform);
}

// 设置 SVG 画布的宽高，并且支持缩放
const width = 4000;
const height = 8000;
const zoom = d3.zoom()
    .scaleExtent([0.5, 5])  // 设置缩放范围
    .on("zoom", zoomed);  // 调用 zoomed 函数

// 创建 SVG 容器，并启用缩放功能
const svg = d3.select("svg")
    .attr("width", width)
    .attr("height", height)
    .call(zoom);  // 绑定缩放功能

let bubbles;  // 定义 bubbles 变量作为全局变量

// 加载数据
d3.csv("listeners.csv").then(data => {
    // 确保数值为数字类型
    data.forEach(d => {
        d.Listeners = +d.Listeners.replace(/,/g, '');
        d["Daily Trend"] = +d["Daily Trend"].replace(/,/g, '');
        d.PkListeners = +d.PkListeners.replace(/,/g, '');
    });

    // 设置初始视图为视图1
    updateView("view1");

    // 添加按钮事件监听
    d3.select("#view1").on("click", () => updateView("view1"));
    d3.select("#view2").on("click", () => updateView("view2"));
    d3.select("#view3").on("click", () => updateView("view3"));

    function updateView(view) {
        // 清除之前的图形
        svg.selectAll("*").remove();

        let size, color, opacity;

        if (view === "view1") {
            size = d => d.Listeners;
            const colorScale = d3.scaleLinear()
            .domain([d3.min(data, d => d.Listeners), d3.max(data, d => d.Listeners)])
            .range(["lightblue", "red"]);  // 小气泡为浅蓝色，大气泡为红色
            color = d => colorScale(d.Listeners);  // 使用基于气泡大小的颜色映射
            opacity = () => 1;  // 默认不调整透明度
        } else if (view === "view2") {
            size = d => d["Daily Trend"]**(1.45);
            const colorScale = d3.scaleLinear()
                .domain([d3.min(data, d => d["Daily Trend"]), d3.max(data, d => d["Daily Trend"])])
                .range(["blue", "red"]);

            // 基于 Daily Trend 的绝对值设置透明度比例尺
            const opacityScale = d3.scaleLinear()
                .domain([0, d3.max(data, d => Math.abs(d["Daily Trend"]))])  // 绝对值的范围
                .range([0.5, 1]);  // 最低为 0.1，最高为 1 的透明度

            color = d => colorScale(d["Daily Trend"]);  // 颜色映射为函数
            opacity = d => opacityScale(Math.abs(d["Daily Trend"]));  // 透明度映射为函数
        } else if (view === "view3") {
            size = d => d.PkListeners;
            const colorScale = d3.scaleLinear()
                .domain([d3.min(data, d => d.PkListeners), d3.max(data, d => d.PkListeners)])
                .range(["purple", "yellow"]);
            color = d => colorScale(d.PkListeners);  // 使用基于气泡大小的颜色映射
            opacity = () => 1;  // 默认不调整透明度
        }

        // 定义 bubbles 变量
        bubbles = svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("r", d => Math.sqrt(size(d) / 1000))  // 放大气泡大小差异
            .attr("fill", d => color(d))  // 使用 color 函数来确定颜色
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .attr("opacity", d => opacity(d))  // 使用 opacity 函数来设置透明度
            .on("mouseover", (event, d) => {
                // 显示气泡信息并在气泡旁边显示
                const tooltip = d3.select("body").append("div")
                    .attr("class", "tooltip")
                    .style("position", "absolute")
                    .style("background", "white")
                    .style("border", "1px solid black")
                    .style("padding", "50px")
                    .style("font-size", "50px")  // 增大字体大小
                    .style("pointer-events", "none")
                    .html(`${d.Artist}<br>听众数: ${d.Listeners}<br>每日趋势: ${d["Daily Trend"]}<br>峰值听众数: ${d.PkListeners}`);
        
                // 将工具提示放置在鼠标旁边
                tooltip
                    .style("left", (event.pageX + 10) + "px")  // 设置距离鼠标位置的偏移量
                    .style("top", (event.pageY - 20) + "px");  // 设置在气泡旁边
            })
            .on("mousemove", (event, d) => {
                // 当鼠标移动时，更新工具提示的位置
                d3.select(".tooltip")
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 20) + "px");
            })
            .on("mouseout", () => {
                // 移除工具提示
                d3.select(".tooltip").remove();
            });

        // 创建气泡布局
        const simulation = d3.forceSimulation(data)
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("charge", d3.forceManyBody().strength(d => -Math.sqrt(size(d) / 500)))  // 根据大小调整中心力
            .force("collision", d3.forceCollide().radius(d => Math.sqrt(size(d) / 10000) + 50))  // 调整碰撞半径，差异更大
            .on("tick", ticked);  // 在 bubbles 定义之后调用 ticked 函数
    }

    // 更新气泡位置
    function ticked() {
        bubbles
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    }
});
