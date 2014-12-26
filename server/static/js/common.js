function bind_homepage() {
    $("#homepage-btn").bind('click', function(){
        window.location.href = '/static/web/homepage.html'
    });
}

function bind_hover(id) {
    $(id).hover(
            function(){
                $(this).addClass('hover');
                $(this).removeClass('unhover');
            },  
            function(){
                $(this).addClass('unhover');
                $(this).removeClass('hover');
            });
}

function waitingInit() {
    var WAITING_WIDTH = 170;
    var WAITING_HEIGHT = 50;
    var text = $("<p></p>", {"style":"text-align:center; font-size:14px; margin-bottom:0px; color: gray;"});
    text.append("Please wait...");
    $('#waiting')[0].style.overflow = "visible";
    $('#waiting').append(text);
    $('#waiting').dialog({modal:true, width:WAITING_WIDTH, height:WAITING_HEIGHT, position:[(document.body.clientWidth-WAITING_WIDTH)/2, (document.body.clientHeight-WAITING_HEIGHT+400)/2]});
    $(".ui-dialog-titlebar").hide();
    $('#waiting').dialog("close");
}

function waitingShow() {
    $('#waiting').dialog("open");
}

function waitingHide() {
    $('#waiting').dialog("close");
}

