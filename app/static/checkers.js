
// Declaring font awesome classes for the different pieces
const KING = "fa-dot-circle fa-5x";
const NORMAL = "fa-circle fa-5x";
const RED = "far";
const BLACK = "fas";


function boardState(){
    var board;
    $.ajax({url: $SCRIPT_ROOT + '/api/board', success: function(result){
        renderBoardState(result);
    }});
}

function renderBoardState(json){
    for (item in json.tiles){
        // console.log(json.tiles[item]);
        const color = json.tiles[item].color;
        renderTile(item, color, json.tiles[item].king)
        // $(` #${item} `).text(json.tiles[item].color);
    }
}

function renderTile(tile, color, king){
    var icon = $(`#${tile} > i`)
    icon.removeClass(); // removes all classes
    if(color == 'Red'){
        if(king){
            icon.addClass(`${RED} ${KING}`);
        }
        else{
            icon.addClass(`${RED} ${NORMAL}`);
        }
    }
    else if(color == 'Black'){
        if(king){
            icon.addClass(`${BLACK} ${KING} `);
        }
        else{
            icon.addClass(`${BLACK} ${NORMAL}`);
        }
    }
    else if(color == 'None'){
        icon.addClass(`hidden`);
    }
    else{
        // idk lol shouldn't be this
    }
}

function selected(){
    $(this).addClass("selected")
}

$( document ).ready(function(){
    boardState();
    $(".clickabletd").click(selected);
});