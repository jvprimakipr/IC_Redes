function print(p){
    console.log(p);
}

function randInt(a,b){
    return a+Math.floor(Math.random()*(b+1-a));
}

function cos(angle){
    return Math.cos(angle*(Math.PI/180));
}
function sin(angle){
    return Math.sin(angle*(Math.PI/180));
}

function create(typeSVG,info){
    var xmlns = "http://www.w3.org/2000/svg";
    var newE = document.createElementNS(xmlns,typeSVG);
    for(var i in info){
        newE.setAttribute(i,info[i]);
    }
    return newE;
}