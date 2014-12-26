function bind_start() {
    $('#start').bind('click', function(){
        //window.location.href = '/static/web/view.html'
        //window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://www.stressanalyser.com/api/code';
        window.location.href = 'https://api.weibo.com/oauth2/authorize?client_id=118376207&response_type=code&redirect_uri=http://localhost:8080/api/code';
    });
}
$(document).ready(function(){
    bind_hover('#start');
    bind_start();
    bind_homepage();
});
