var mainSVG = document.getElementById("svg");
var width = mainSVG.width.animVal.value;
var height = mainSVG.height.animVal.value;

var st = create("rect",{id:"st", x:"0", y:"0", width:width, height:height, fill:"transparent", stroke:"black", "stroke-width":3});
mainSVG.appendChild(st);
var projetor =1;
if (projetor===1){
    Edge.defaultColor = "rgb(0, 0, 255)";
}
var translate = {"Selecione a organização":"","Por grau":"degree"};

var graph = new Graph("svg");

function updateInfo(){
    Graph.animation = document.getElementById("animation").checked;
    var delay = document.getElementById("delay").checked;
    if (delay){
        Graph.delay = 2000;
    }
    else{
        Graph.delay = 0;
    }
}
function loadGraph(){
    updateInfo();
    var movie = document.getElementById("graphMovie").value;
    if (movie=="Homem de Ferro 1"){
        graph.load();
        var data;
	    Papa.parse(fileInput.files[0], {
            complete: function(results) {
                console.log(results);
            }
        });
        print(data);
    }
}
function clean(){
    graph.reset();
}
function resetTransf(){
    graph.infoTransf = {t:{x:0,y:0}};
    graph.updateTransf();
}
function newRank(){
    updateInfo();
    if (graph.hasElements){
        var rankType = translate[document.getElementById("rankType").value];
        graph.newRank(rankType);
    }
}

$("body").keydown(function (evt){
    updateInfo();
    //Tecla P
    if (evt.keyCode===80){
        graph.ableToCreatePath = true;
    }
})

$("body").keyup(function (evt){
    updateInfo();
    //Tecla P
    if (evt.keyCode===80){
        graph.ableToCreatePath = false;
    }
})