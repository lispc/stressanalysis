var URL_STRESS = '/api/get_stress';
var URL_STRESS_TIME = '/api/get_stress_by_time';
var URL_KEYWORD = '/api/get_keyword';
var NUMBER = 5;
var type = 1;
var step = 1;

function bind_select() {
    for (var i=1; i<=NUMBER; i++) {
        var btn = '#s-' + i;
        $(btn)[0].o = i;
        $(btn).bind('click', function(){
            $('#step-'+type+'-'+step).hide();
            $('#l-'+type).hide();
            $('#step-'+this.o+'-1').show();
            $('#l-'+this.o).show();
            type=this.o;
            step = 1;
        });
    }
}

function bind_all_hover() {
    bind_hover('.btn-stress');
}

function load_stress() {
    waitingShow();
    $.get(URL_STRESS, {}, function(data){
        if (data.success == -1) {
            //window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://localhost:8080/api/code';
            window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://localhost:8080/api/code';
        }
        if (data.success == 1) {
            var name = data.name;
            var src = data.src;
            $('#step-1-2 .person-name').html(name);
            $('#step-1-2 .person-img').attr('src', src);
            var s = parseInt(data.stress*100);
            var color = 'green';
            if (s > 20) color = 'blue';
            if (s > 50) color = 'orange';
            if (s > 80) color = 'red';
            $('#report-div').highcharts({
                chart: {type: 'column', height: 300, width: 150},
                title: {text: '', x:0},
                xAxis: {categories: [s+'%'],
                    labels: {style: {fontSize: '30px', fontFamily: 'Helvetica Neue', 
                        color: color}, y:45}},
                yAxis: {min: 0, max: 100, title: {text: ''}},
                legend: {enabled: false},
                tooltip: {enabled: false},
                series: [{name: 'stress', data: [{y: s, color: color}]}]
            });
            $('#reason-div').highcharts({
                chart: {height: 400, width: 400},
                title: {text: '', x:0},
                legend: {enabled: false},
                tooltip: {enabled: false},
                series: [{type: 'pie',data: data.reason}]
            });
            $('tspan:contains(Highcharts.com)').hide();
        }
        waitingHide();
    }, 'json');
}

function load_stress_time() {
    var from = parseInt(new Date().getTime()) - 7*24*3600*1000;
    var until = parseInt(new Date().getTime());
    waitingShow();
    $.get(URL_STRESS_TIME, {from: from, until: until}, function(data){
        if (data.success == -1) {
            window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://localhost:8080/api/code';
        }
        if (data.success == 1) {
            var name = data.name;
            var src = data.src;
            $('#step-2-2 .person-name').html(name);
            $('#step-2-2 .person-img').attr('src', src);
            var x = [];
            var y = [];
            for (var j=0; j<data.data.length; j++) {
                x.push(data.data[j].time);
                y.push(data.data[j].stress);
            }
            function formatAuto() {
                return new Date(this.value).format('mm-dd');
            }
            $('#line-div').highcharts({
                chart: {height: 320, width: 550},
                title: {text: '', x:0},
                xAxis: {categories: x, labels: {formatter: formatAuto}},
                yAxis: {min: 0, title: {text: ''}},
                legend: {enabled: false},
                tooltip: {enabled: false},
                series: [{data:y, name: 'stress value'}]
            });
            $('tspan:contains(Highcharts.com)').hide();
            waitingHide();
        }
    }, 'json');
}

function load_keywords() {
    var limit = 20;
    waitingShow();
    $.get(URL_KEYWORD, {limit: limit}, function(data){
        if (data.success == -1) {
            window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://localhost:8080/api/code';
        }
        if (data.success == 1) {
            var name = data.name;
            var src = data.src;
            $('#step-3-2 .person-name').html(name);
            $('#step-3-2 .person-img').attr('src', src)
            var s = $("#keyword-div");
            s.html('');
            for (var i=0; i<data.data.length; i++) {
                if (i > 10) break;
                s.append($("<p></p>").text(data.data[i].keyword+' '+data.data[i].weight));
            }
        }
        waitingHide();
    }, 'json');
}

function next_step() {
    $('#step-'+type+'-'+step).hide();
    step += 1;
    $('#step-'+type+'-'+step).show();
}

function bind_all_click() {
    $("div[name=next]").bind("click", function(){next_step()});
    $("#youself-1").bind("click", function(){load_stress()});
    $("#youself-2").bind("click", function(){load_stress_time()});
    $("#youself-3").bind("click", function(){load_keywords()});
}

$(document).ready(function() {
    waitingInit();
    bind_select();
    bind_homepage();
    bind_all_hover();
    bind_all_click();
});

