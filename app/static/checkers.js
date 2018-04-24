function boardState(){
    var board;
    $.ajax({url: $SCRIPT_ROOT + '/api/board', success: function(result){
        renderBoardState(result);
    }});
}

function renderBoardState(json){
    for (item in json.tiles){
        // console.log(json.tiles[item]);
        $(` #${item} `).text(json.tiles[item].color);
    }
}

function selected(){
    $(this).addClass("selected")
}

$( document ).ready(function(){
    boardState();
    $(".clickabletd").click(selected);
});