function boardState(){
    $.ajax({url: $SCRIPT_ROOT + '/api/board', success: function(result){
        for(var item in result.tiles){
            console.log(result.tiles[item]);
        }
    }});
}

$( document ).ready(function(){
    boardState();
});