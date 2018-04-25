
// Declaring font awesome classes for the different pieces
const KING = "fa-dot-circle fa-5x";
const NORMAL = "fa-circle fa-5x";
const RED = "fas";
const BLACK = "far";
var selectedTile;
var currentTurn

// renders the board
function boardState(){
    getCurrentTurn();
    var board;
    $.ajax({url: $SCRIPT_ROOT + '/api/board', success: function(result){
        renderBoardState(result);
    }});
}

// takes json of board state and renders the board. event handler for boardState
// also assigns on click handlers
function renderBoardState(json){
    for (item in json.tiles){
        const color = json.tiles[item].color;
        console.log(`current turn ${currentTurn} color ${color}`);
        if(currentTurn == color){
            $(`#${item}`).click(selected);
        }
        renderTile(item, color, json.tiles[item].king)
    }
}

// sets the global variable current turn to the current turn
function getCurrentTurn(){
    $.ajax({url: $SCRIPT_ROOT + '/api/stats', success: setCurrentTurn});
}

function setCurrentTurn(result){
    console.log(currentTurn);
    currentTurn = result.turn;
    console.log(currentTurn);
}

// renders a tile properly
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

// the on click when you choose a tile
function selected(){
    selectedTile = $(this).attr("id");
    $(this).addClass("selected");
    $.ajax({url: $SCRIPT_ROOT + '/api/legal', 
    method:"POST",
    data: {
        'start': $(this).attr("id")
    },
    success: function(result){
        renderClickable(result);
        $(`#${result.startPoint}`).click(unselect);
    }});
}

function unselect(){
    $(".clickabletd").off("click");
    $(this).removeClass('selected');
    $('.legalLocation').removeClass('legalLocation');
    boardState()
}

// The next 3 functions work as a group in order to handle moving of tiles

function renderClickable(result){
    $(".clickabletd").off("click");
    console.log(result);
    for(var id in result.endPoints){
        console.log(id);
        $(`#${id}`).addClass('legalLocation');
        addClickableTile(id, selectedTile);
    }
    selectedTile = null;
}

function addClickableTile(id, startId){
    $(`#${id}`).click(function(){
        movePiece(id, startId)
    });
}

function movePiece(id, startId){
    $('.selected').removeClass('selected');
    $('.legalLocation').removeClass('legalLocation');
    selectedTile = null;
    $.ajax({url: $SCRIPT_ROOT + '/api/move', 
    method:"POST",
    data: {
        'start': startId,
        'end': id
    },
    success: function(result){
        boardState();
    }});
}

// main
$( document ).ready(function(){
    boardState();
});