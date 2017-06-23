/**
 * Created by sunhaoran on 2017/6/22.
 */

var searchType = "ftxt";

$('.searchButton').click(function(){
    var history = $.cookie('history');
    history += $('.searchInput').val()+',';
    $.cookie('history', history);
    window.location = 'result.html?searchtype=ftxt&query=' + $('.searchInput').val();
});

$('.search').click(function(){
    var history = $.cookie('history');
    history += $('#stxt').val()+',';
    $.cookie('history', history);
    var col="";
    for(var i=0;i<6;i++){
        if($('.coln input[type=checkbox]').eq(i).prop('checked')){
            col+=$('.coln input[type=checkbox]').eq(i).attr('id')+',';
        }
    }
    if(col!=""){
        col=col.substr(0, col.length-1);
        window.location = 'result.html?searchtype=' + searchType + '&query=' + $('#stxt').val() + '&region=' + col;
    } else {
        window.location = 'result.html?searchtype=' + searchType + '&query=' + $('#stxt').val();
    }

});

$('.qod input[type=radio]').click(function(e) {
    if($(this).prop('checked')){
        searchType = $(this).attr('id');
    }
});

setHeight();
$(window).resize(function(){
    setHeight();
});

function setHeight(){
    if($('#container').outerHeight() < $(window).height()){
        $('#container').height($(window).height()-33);
    }
}