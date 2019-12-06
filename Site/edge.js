class Edge{
    constructor(myidgraph,myidNode1,myidNode2){
        //Basics
        this.id = "edge"+Edge.getCurrentId();
        Edge.setCurrentId();
        this.idGraph = myidgraph;
        Graph.getGraphById(this.idGraph).setListOfEdges(this.id,this);
        //About source and target
        this.idSource = myidNode1;
        this.idTarget = myidNode2;
        var infoInit = {id:this.id,stroke:Edge.defaultColor,"stroke-width":"2",cursor:"pointer"};
        var source = document.getElementById(this.idSource);
        var target = document.getElementById(this.idTarget);
        infoInit.x1 = source.getAttribute("cx");
        infoInit.y1 = source.getAttribute("cy");
        infoInit.x2 = target.getAttribute("cx");
        infoInit.y2 = target.getAttribute("cy");
        this.SVG = create("line",infoInit);
        Graph.getGraphById(this.idGraph).getNodeById(this.idSource).edges = this.id;
        Graph.getGraphById(this.idGraph).getNodeById(this.idTarget).edges = this.id;
        //Others
        this.drawed = false;
        this.workMouse();
    }
    //Id that will be used for new edge
    static currentId = 1;
    static setCurrentId(){
        Edge.currentId += 1;
    }
    static getCurrentId(){
        return Edge.currentId;
    }
    //Draw the edge
    draw(){
        Graph.getGraphById(this.idGraph).SVG.appendChild(this.SVG);
        Graph.getGraphById(this.idGraph).drawAllNodes();
        this.drawed = true;
    }
    //Remove the edge
    remove(){
        if (this.drawed){
            Graph.getGraphById(this.idGraph).SVG.removeChild(this.SVG);
        }
    }
    //Overlap the edge
    overlap(){
        this.remove();
        this.draw();
    }
    //Animate the edge
    animate(){
        this.SVG.setAttribute("stroke","rgb(179, 218, 255)");
        this.draw();
        var _this = this;
        var totalSteps = 400;
        var step = 0;
        var newEdge = create("line",{x1:this.SVG.getAttribute("x1"),y1:this.SVG.getAttribute("y1"),
            x2:this.SVG.getAttribute("x1"),y2:this.SVG.getAttribute("y1"),stroke:Edge.defaultColor,
            "stroke-width":"2",cursor:"pointer"});
        Graph.getGraphById(this.idGraph).SVG.appendChild(newEdge);
        var edgeAnimInterval = setInterval(function(){
            let vector = {x:_this.SVG.getAttribute("x2")-_this.SVG.getAttribute("x1"),
            y:_this.SVG.getAttribute("y2")-_this.SVG.getAttribute("y1")};
            let newx2 = parseFloat(_this.SVG.getAttribute("x1"))+vector.x*step/totalSteps;
            let newy2 = parseFloat(_this.SVG.getAttribute("y1"))+vector.y*step/totalSteps;
            newEdge.setAttribute("x2",newx2);
            newEdge.setAttribute("y2",newy2);
            Graph.getGraphById(_this.idGraph).getNodeById(_this.idSource).overlap();
            step += 1;
            if (step===totalSteps){
                Graph.getGraphById(_this.idGraph).SVG.removeChild(newEdge);
                _this.SVG.setAttribute("stroke",Edge.defaultColor);
                clearInterval(edgeAnimInterval);
            }
        },1)
    }
    //Update the edge
    update(){
        var source = document.getElementById(this.idSource);
        var target = document.getElementById(this.idTarget);
        this.SVG.setAttribute("x1",source.getAttribute("cx"));
        this.SVG.setAttribute("y1",source.getAttribute("cy"));
        this.SVG.setAttribute("x2",target.getAttribute("cx"));
        this.SVG.setAttribute("y2",target.getAttribute("cy"));
    }
    //Color functions
    //Default color of edge
    static defaultColor = "rgb(0, 48, 102)";
    //Change color of edge
    changeColor(newColor = Edge.defaultColor){
        this.SVG.setAttribute("stroke",newColor);
    }
    //Mouse functions
    workMouse(){
        var auxId = this.idGraph;
        this.SVG.onmouseenter = function(){
            Graph.getGraphById(auxId).getEdgeById(this.getAttribute("id")).mouseEnter();
        }
        this.SVG.onmouseleave = function(){
            Graph.getGraphById(auxId).getEdgeById(this.getAttribute("id")).mouseLeave();
        }
    }
    mouseEnter(){
        this.changeColor("rgb(230,0,0)");
        Graph.getGraphById(this.idGraph).getNodeById(this.idSource).overlap();
        Graph.getGraphById(this.idGraph).getNodeById(this.idSource).changeColor("rgb(230,0,0)");
        Graph.getGraphById(this.idGraph).getNodeById(this.idTarget).overlap();
        Graph.getGraphById(this.idGraph).getNodeById(this.idTarget).changeColor("rgb(230,0,0)");
    }
    mouseLeave(){
        this.changeColor();
        Graph.getGraphById(this.idGraph).getNodeById(this.idSource).changeColor();
        Graph.getGraphById(this.idGraph).getNodeById(this.idTarget).changeColor();
    }
}