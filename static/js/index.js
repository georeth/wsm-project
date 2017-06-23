/**
 * Created by sunhaoran on 2017/6/22.
 */

var searchType = "ftxt";

$(function(){
    var his = "";
    var h = $.cookie('history');
    h = h.substr(0, h.length-1);
    var history = h.split(",");
    for(var i=0;i<history.length;i++){
        his += '<span>' + history[i] + '  </span>';
    }
    $('.myhis').append(his);
});

$('.searchList').on('click', '.searchItem', function(){
    $('.searchList .searchItem').removeClass('current');
    $(this).addClass('current');
    searchType = $(this).attr('id');
});

// // 联想下拉显示隐藏
// $('.searchInput').on('focus', function(){
//     $('.dataList').show();
// });
//
// // 联想下拉点击
// $('.dataList').on('click', 'li', function(){
//     var text = $(this).text();
//     $('.searchInput').val(text);
//     $('.dataList').hide();
// });
//
// hideElement($('.dataList'), $('.searchInput'));

$('.searchButton').click(function(){
    var history = $.cookie('history');
    history += $('.searchInput').val()+',';
    $.cookie('history', history);
    window.location = 'result.html?searchtype=' + searchType + '&query=' + $('.searchInput').val();
});