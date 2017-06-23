/**
 * Created by sunhaoran on 2017/6/22.
 */

var searchType = "";
var searchRegion = "";
var args;

$(function(){
    var his = "";
    var h = $.cookie('history');
    h = h.substr(0, h.length-1);
    var history = h.split(",");
    for(var i=0;i<history.length;i++){
        his += '<li>' + history[i] + '  </li>';
    }
    $('.historyList').append(his);

    args = getUrlParam();
    searchType = args['searchtype'];
    if(args['region'] != null){
        searchRegion = args['region'];
    }

    $('.searchInput').val(args['query']);
    $('.searchList .searchItem').removeClass('current');
    $('#'+searchType).addClass('current');

    querysearch(args['query']);
});

$('.searchButton').click(function(){
    var history = $.cookie('history');
    history += $('.searchInput').val()+',';
    $.cookie('history', history);
    window.location = 'result.html?searchtype=' + searchType + '&query=' + $('.searchInput').val();
});

$('.searchList').on('click', '.searchItem', function(){
    $('.searchList .searchItem').removeClass('current');
    $(this).addClass('current');
    searchType=$(this).attr('id');

    querysearch(args['query']);
});

function querysearch(s){
    var result="";
    $('.resultList').html(result);
    
    var postdata = new Object();
    postdata.s = s;
    if(searchRegion != ""){
        postdata.region=searchRegion.split(",");
    }
    if(searchType == 'docr'){
        postdata.type = 'doctor';
    }else if(searchType == 'qas'){
        postdata.type = 'question';
    }

    $.ajax({
        type: 'POST',
        url: searchAllUrl,
        crossDomain: true,
        contentType: "application/json",
        dataType: "JSON",
        data: JSON.stringify(postdata),
        success: function (data) {
            for(var i = 0; i < data.length; i++){
                if(data[i].type == 'question'){
                    var title = data[i].title.split('\n\t\t');
                    result += '<div class="resultItem">'
                        + '<div class="itemHead">'
                        + '<a class="title">' + title[1] + '</a>'
                        + '<span class="divsion">-</span>'
                        + '<span class="fileType">'
                        + '<span class="label">问题分类：</span>'
                        + '<span class="value">' + title[0] + '</span>'
                        + '</span>'
                        + '</div>'
                        + '<div class="itemBody"><span class="itemHead">问题详情： </span>' + data[i].detail + '</div>';

                    for(var j=0; j<data[i].reply_list.length; j++){
                        result += '<div class="itemBody"><span class="itemAns"><span style="color: #ff9b0c;">医生回答： </span>'
                            + data[i].reply_list[j].detail + '</span>'
                            + '<div class="itemFoot">'
                            + '<span class="info">'
                            + '<label>医生：</label>'
                            + '<span class="value">' + data[i].reply_list[j].doctor_infos[0] + '</span>'
                            + '</span>'
                            + '</div>'
                            + '</div>';
                    }
                }else if(data[i].type == 'doctor'){
                    result += '<div class="resultItem">'
                        + '<div class="itemHead">'
                        + '<a class="title">' + data[i].name + '</a>'
                        + '<span class="divsion">-</span>'
                        + '<span class="fileType">'
                        + '<span class="label">所属科室：</span>'
                        + '<span class="value">' + data[i].department + '</span>'
                        + '</span>'
                        + '<span class="dependValue">'
                        + '<span class="label">职位：</span>'
                        + '<span class="value">' + data[i].title + '</span>'
                        + '</span>'
                        + '</div>'
                        + '<div class="itemBody">' + data[i].profile + '</div>'
                        + '<div class="itemBody">' + data[i].expert + '</div>'
                        + '<div class="itemFoot">'
                        + '<span class="info">'
                        + '<span class="value">' + data[i].hospital + '</span>'
                        + '</span>'
                        + '</div>'
                        + '</div>';
                }
            }
            $('.resultList').append(result);
        }
    });
}

$.each($('.subfieldContext'), function(i, item){
    //$(this).find('li:gt(2)').hide().end().find('li:last').show();
});

$('.subfieldContext .name').click(function(){
    searchRegion = $(this).attr('id');
    querysearch(args['query']);
});

$('.sideBarShowHide a').click(function(e) {
    if($('#main').hasClass('sideBarHide')){
        $('#main').removeClass('sideBarHide');
        $('#container').removeClass('sideBarHide');
    }else{
        $('#main').addClass('sideBarHide');
        $('#container').addClass('sideBarHide');
    }

});

// //分页
// $(".pagination").pagination(500, {
//     current_page :0, //当前页码
//     items_per_page :9,
//     display_msg :true,
//     callback :pageselectCallback
// });
// function pageselectCallback(page_id, jq) {
//     alert("当前页id(由0开始)：" + page_id + "，\n每页显示：" + this.items_per_page + "条数据");
// }

setHeight();
$(window).resize(function(){
    setHeight();
});

function setHeight(){
    if($('#container').outerHeight() < $(window).height()){
        $('#container').height($(window).height()-33);
    }
}

//获取url参数
function getUrlParam() {
    var args = new Object();
    var query = decodeURI(location.search.substring(1));//获取查询串

    var pairs = query.split("&");//在逗号处断开

    for (var i = 0; i < pairs.length; i++) {

        var pos = pairs[i].indexOf('=');//查找name=value

        if (pos == -1)   continue;//如果没有找到就跳过

        var argname = pairs[i].substring(0, pos);//提取name

        var value = pairs[i].substring(pos + 1);//提取value

        args[argname] = unescape(value);//存为属性

    }

    return args;
}
