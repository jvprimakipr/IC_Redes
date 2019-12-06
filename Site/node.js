class Node{
    constructor(myidgraph,mycx,mycy,myname=""){
        //Basics
        this.id = "node"+Node.getCurrentId();
        Node.setCurrentId();
        this.idGraph = myidgraph;
        this.r = Node.defaultRadius;
        Graph.getGraphById(this.idGraph).setListOfNodes(this.id,this);
        var infoInit = {id:this.id,cx:mycx,cy:mycy,r:this.r,fill:Node.defaultColor,stroke:"black","stroke-width":"1",cursor:"pointer"};
        this.SVG = create("circle",infoInit);
        this.drawed = false;
        this._edges = [];
        this.degree = 0;
        this.following = false;
        this.workMouse();
    }
    //Id that will be used for new node
    static currentId = 1;
    static setCurrentId(){
        Node.currentId += 1;
    }
    static getCurrentId(){
        return Node.currentId;
    }
    //Draw the node
    draw(){
        Graph.getGraphById(this.idGraph).SVG.appendChild(this.SVG);
    }
    //Remove the node
    remove(){
        Graph.getGraphById(this.idGraph).SVG.removeChild(this.SVG);
    }
    //Overlap the node
    overlap(){
        this.remove();
        this.draw();
    }
    //About edges of this node
    get edges(){
        return this._edges;
    }
    set edges(n){
        this._edges.push(n);
        this.degree += 1;
        Graph.getGraphById(this.idGraph).setMaxDegree(this.degree);
    }
    //Color functions
    //Default color of node
    static defaultColor = "rgb(150,150,150)";
    //Change color of node
    changeColor(newColor = Node.defaultColor){
        this.SVG.setAttribute("fill",newColor);
    }
    //Radius functions
    static defaultRadius = 5;
    static maxRadius = 30;
    //Animate the node
    animate(){
        var auxRadius = Node.defaultRadius;
        var _this = this;
        var nodeAnimInterval = setInterval(function(){
            if (auxRadius>=_this.r){
                clearInterval(nodeAnimInterval);
            }
            else{
                _this.SVG.setAttribute("r",auxRadius);
                auxRadius += 1;
            }
        },50)
    }
    //Position functions
    follow(dot){
        var coord = Graph.getGraphById(this.idGraph).getInverseTransf(dot.offsetX,dot.offsetY);
        this.SVG.setAttribute("cx",coord.x);
        this.SVG.setAttribute("cy",coord.y);
        //this.SVG.setAttribute("transform",Graph.getGraphById(this.idGraph).getInverseTransf());
        for (var i=0;i<this.edges.length;i++){
            Graph.getGraphById(this.idGraph).getEdgeById(this.edges[i]).update();
        }
    }
    //Mouse functions
    workMouse(){
        var auxId = this.idGraph;
        this.SVG.onmouseenter = function(){
            Graph.getGraphById(auxId).getNodeById(this.getAttribute("id")).mouseEnter();
        }
        this.SVG.onmouseleave = function(){
            Graph.getGraphById(auxId).getNodeById(this.getAttribute("id")).mouseLeave();
        }
        this.SVG.onmousedown = function(){
            Graph.getGraphById(auxId).getNodeById(this.getAttribute("id")).mouseDown();
        }
        this.SVG.onmouseup = function(){
            Graph.getGraphById(auxId).getNodeById(this.getAttribute("id")).mouseUp();
        }
        this.SVG.onmousemove = function(evt){
            Graph.getGraphById(auxId).getNodeById(this.getAttribute("id")).mouseMove(evt);
        }
    }
    mouseEnter(){
        this.changeColor("rgb(230,0,0)");
        for (var i=0;i<this.edges.length;i++){
            Graph.getGraphById(this.idGraph).getEdgeById(this.edges[i]).overlap();
            Graph.getGraphById(this.idGraph).getEdgeById(this.edges[i]).changeColor("rgb(230,0,0)");
        }
        this.overlap();
    }
    mouseLeave(){
        this.changeColor();
        for (var i=0;i<this.edges.length;i++){
            Graph.getGraphById(this.idGraph).getEdgeById(this.edges[i]).changeColor();
        }
    }
    mouseDown(){
        this.following = true;
        this.SVG.setAttribute("cursor","grabbing");
        Graph.getGraphById(this.idGraph).idChoosenNode = this.id;
    }
    mouseUp(){
        this.following = false;
        this.SVG.setAttribute("cursor","pointer");
        Graph.getGraphById(this.idGraph).idChoosenNode = "";
    }
    mouseMove(evt){
        if(this.following){
            this.follow(evt);
        }
    }
    //Rank functions
    rankByDegree(limit=false){
        if (limit){
            this.r = Node.defaultRadius+(this.degree/limit)*(Node.maxRadius-Node.defaultRadius);
            if (Graph.animation){
                this.animate();
            }
            else{
                this.SVG.setAttribute("r",this.r);
            }
        }
        else{
            this.r = Node.defaultRadius+this.degree;
            if (Graph.animation){
                this.animate();
            }
            else{
                this.SVG.setAttribute("r",this.r);
            }
        }
    }
}