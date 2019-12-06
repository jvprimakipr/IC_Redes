class Graph{
    constructor(mysvg){
        //SVG that will be used for graph
        this.mainSVG = document.getElementById(mysvg);
        this.width = this.mainSVG.width.animVal.value;
        this.height = this.mainSVG.height.animVal.value;
        //Basics
        this.id = "graph"+Graph.getCurrentId();
        Graph.setCurrentId();
        Graph.setListOfGraphs(this.id,mysvg,this);
        this.variables();
    }
    variables(){
        //Basics Elements
        this.SVG = create("g",{id:this.id});
        this.mainSVG.appendChild(this.SVG);
        this.listOfNodes = {};
        this.idChoosenNode = "";
        this.maxDegree = 0;
        this.listOfEdges = {};
        this.hasElements = false;
        this.loadingGraph = false;
        this.ableToCreatePath = false;
        this.workMouse();
        //Transformations: Translate t, Rotate r, Scale s
        this.translating = false;
        this.dotTranslate = {x:0,y:0};
        this.oldTranslate = {x:0,y:0};
        this.infoTransf = {t:{x:0,y:0}};
    }
    //Id that will be used for new node
    static currentId = 1;
    static setCurrentId(){
        Graph.currentId += 1;
    }
    static getCurrentId(){
        return Graph.currentId;
    }
    //HTML informations
    static animation = false;
    static delay = 0;
    //About main SVG
    setMainSVG(myid){
        this.mainSVG = document.getElementById(myid);
        this.width = this.mainSVG.width.animVal.value;
        this.height = this.mainSVG.height.animVal.value;
    }
    getMainSVG(){
        return this.mainSVG;
    }
    //About list of graphs
    static listOfGraphs = {};
    static setListOfGraphs(myid,myidms,mygraph){
        Graph.listOfGraphs[myid] = mygraph;
        Graph.listOfGraphs[myidms] = mygraph;
    }
    static getListOfGraphs(){
        return Graph.listOfGraphs;
    }
    static getGraphById(myid){
        return Graph.listOfGraphs[myid];
    }
    static getGraphByIdMS(myid){
        return Graph.listOfGraphs[myid];
    }
    //Reset the entire graph
    reset(){
        this.getMainSVG().removeChild(this.SVG);
        this.variables();
    }
    //About list of nodes
    setListOfNodes(myid,mynode){
        this.listOfNodes[myid] = mynode;
        if (this.hasElements===false){
            this.hasElements = true;
        }
    }
    getListOfNodes(){
        return this.listOfNodes;
    }
    getNodeById(myid){
        return this.listOfNodes[myid];
    }
    getLastNode(){
        var auxId = Object.keys(this.getListOfNodes())[Object.keys(this.getListOfNodes()).length];
        return this.listOfNodes[auxId];
    }
    setMaxDegree(mydegree){
        this.maxDegree = Math.max(this.maxDegree,mydegree);
    }
    getMaxDegree(){
        return this.maxDegree;
    }
    //Draw all of nodes for they overlap the edges
    drawAllNodes(){
        for (var i in this.getListOfNodes()){
            this.getListOfNodes()[i].overlap();
        }
    }
    //About list of edges
    setListOfEdges(myid,myedge){
        this.listOfEdges[myid] = myedge;
    }
    getListOfEdges(){
        return this.listOfEdges;
    }
    getEdgeById(myid){
        return this.listOfEdges[myid];
    }
    //Transformation functions
    updateTransf(){
        var strTranslate = "translate("+Object.values(this.infoTransf.t).join(" ")+") ";
        this.SVG.setAttribute("transform",strTranslate);
    }
    getInverseTransf(x,y){
        var x1 = x-this.infoTransf.t.x;
        var y1 = y-this.infoTransf.t.y;
        return {x:x1,y:y1};
    }
    //Translate
    translate(evt){
        this.infoTransf.t.x = evt.offsetX-this.dotTranslate.x+this.oldTranslate.x;
        this.infoTransf.t.y = evt.offsetY-this.dotTranslate.y+this.oldTranslate.y;
        this.updateTransf();
        let auxDot = this.getInverseTransf(this.width/2,this.height/2);
        this.dotRotate.x = auxDot.x;
        this.dotRotate.y = auxDot.y;
    }

    //Mouse functions
    workMouse(){
        this.getMainSVG().onmousedown = function(evt){
            Graph.getGraphByIdMS(this.getAttribute("id")).mouseDown(evt);
        }
        this.getMainSVG().onmouseup = function(){
            Graph.getGraphByIdMS(this.getAttribute("id")).mouseUp();
        }
        this.getMainSVG().onmousemove = function(evt){
            Graph.getGraphByIdMS(this.getAttribute("id")).mouseMove(evt);
        }
        this.getMainSVG().onmouseout = function(evt){
            Graph.getGraphByIdMS(this.getAttribute("id")).mouseOut(evt);
        }
        this.getMainSVG().onmousewheel =function(evt){
            Graph.getGraphByIdMS(this.getAttribute("id")).mouseWheel(evt);
        }
    }
    mouseDown(evt){
        this.getMainSVG().setAttribute("cursor","move");
        this.translating = true;
        this.oldTranslate.x = this.infoTransf.t.x;
        this.oldTranslate.y = this.infoTransf.t.y;
        this.dotTranslate.x = evt.offsetX;
        this.dotTranslate.y = evt.offsetY;
    }
    mouseUp(){
        this.getMainSVG().setAttribute("cursor","default");
        this.translating = false;
    }
    mouseMove(evt){
        if (this.idChoosenNode!==""){
            this.getNodeById(this.idChoosenNode).mouseMove(evt);
        }
        else if(this.translating){
            this.translate(evt);
        }
    }
    mouseOut(evt){
        this.getMainSVG().setAttribute("cursor","default");
        this.translating = false;
    }
    //Load functions
    load(reset){
        if (this.loadingGraph===true){
            clearInterval(this.myInterval);
        }
        this.reset();
    }
    //Rank type: degree
    newRank(ranktype){
        if (ranktype==="degree"){
            if (this.getMaxDegree()<=(Node.maxRadius-Node.defaultRadius)){
                for (var i in this.getListOfNodes()){
                    this.getListOfNodes()[i].rankByDegree();
                }
            }
            else{
                for (var i in this.getListOfNodes()){
                    this.getListOfNodes()[i].rankByDegree(this.getMaxDegree());
                }
            }
        }
    }
}
