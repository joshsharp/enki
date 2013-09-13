var initialStatus = "What's happening?"

$(function(){
    $('#timeline-dms').hide();
    $('#timeline-mentions').hide();
    $('#tab-home').addClass('selected');
    $('#tab-dms').click(function(){
        $('#tab-home').removeClass('selected');
        $('#tab-mentions').removeClass('selected');
        $('#tab-dms').addClass('selected');
        $('#timeline-home').hide();
        $('#timeline-dms').show();
        $('#timeline-mentions').hide();
    });
    $('#tab-home').click(function(){
        $('#tab-dms').removeClass('selected');
        $('#tab-mentions').removeClass('selected');
        $('#tab-home').addClass('selected');
        $('#timeline-home').show();
        $('#timeline-dms').hide();
        $('#timeline-mentions').hide();
    });
    
    $('#tab-mentions').click(function(){
        $('#tab-dms').removeClass('selected');
        $('#tab-home').removeClass('selected');
        $('#tab-mentions').addClass('selected');
        $('#timeline-home').hide();
        $('#timeline-dms').hide();
        $('#timeline-mentions').show();
    });
    
    $('#status').val(initialStatus);
    $('#status').addClass('blur');
    
    $('#status').focus(function(){
        $(this).removeClass('blur');
        if ($(this).val() == initialStatus){
            $(this).val('');
            
        }
    });
    
    $('#status').blur(function(){
        
        if ($(this).val() == ''){
            $(this).val(initialStatus);
            $(this).addClass('blur');
        }
    });
    
    $('#status').keydown(function(e){
        if (e.ctrlKey && e.keyCode == 13) {
            
            tweet($(this).val());
            onTweetSuccess();
        }
    });
    
});

function addTweet(tweet){
    $('#timeline-home').prepend(tweet);
}

function addDM(tweet){
    $('#timeline-dms').prepend(tweet);
}

function addMention(tweet){
    $('#timeline-mentions').prepend(tweet);
}

function tweet(text){
    window.connector.tweet(text);
}

function onTweetSuccess(){
    $("#status").val('');
}

function reply(id,text){
    window.connector.tweet(text,id);
}

function dm(screen_name,text){
    window.connector.dm(screen_name,text);
}

function fave(id){
    window.connector.fave(id);
}

function unfave(id){
    window.connector.unfave(id);
}

function delTweet(id){
    window.connector.delete_tweet(id);
}

function delDM(id){
    window.connector.delete_dm(id);
}

function follow(screen_name){
    window.connector.follow(screen_name);
}

function unfollow(screen_name){
    window.connector.unfollow(screen_name);
}

function block(screen_name){
    window.connector.block(screen_name);
}

function spam(screen_name){
    window.connector.spam(screen_name);
}

function viewProfile(screen_name){
    window.connector.view_profile(screen_name);
}

function conversation(id){
    window.connector.show_conversation(id);
}

function preview_url(url){
    window.connector.preview_url(url);
}

function show_sys_menu(){
    var offset = $('#tab-prefs').offset();
    window.connector.show_sys_menu(offset.left,offset.top);
}

function updateTime(id){
    $(".time","t" + id)
}