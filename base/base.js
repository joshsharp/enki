var initialStatus = "What's happening?"

var currentTab = 'home';
var replyID = null;

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
        currentTab = 'dms';
    });
    $('#tab-home').click(function(){
        $('#tab-dms').removeClass('selected');
        $('#tab-mentions').removeClass('selected');
        $('#tab-home').addClass('selected');
        $('#timeline-home').show();
        $('#timeline-dms').hide();
        $('#timeline-mentions').hide();
        currentTab = 'home';
    });
    
    $('#tab-mentions').click(function(){
        $('#tab-dms').removeClass('selected');
        $('#tab-home').removeClass('selected');
        $('#tab-mentions').addClass('selected');
        $('#timeline-home').hide();
        $('#timeline-dms').hide();
        $('#timeline-mentions').show();
        currentTab = 'mentions';
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
            if (currentTab == 'dms') {
                //do something else - prevent tweets
                
                
            } else {
                
                if (replyID != null) {
                    reply(replyID,$(this).val());
                    onTweetSuccess();
                } else {
                    
                    tweet($(this).val());
                    onTweetSuccess();
                }
            }
            
        }
    });
    
});

function addTweet(tweet){
    $('#timeline-home').prepend(tweet);
    if ($('#timeline-home .tweet').length > 300) {
        $('#timeline-home .tweet').last().remove();
    }
}

function addDM(tweet){
    $('#timeline-dms').prepend(tweet);
}

function addMention(tweet){
    $('#timeline-mentions').prepend(tweet);
    if ($('#timeline-mentions .tweet').length > 300) {
        $('#timeline-mentions .tweet').last().remove();
    }
}

function tweet(text){
    window.connector.tweet(text);
}

function onTweetSuccess(){
    $("#status").val('');
    replyID = null;
    $('#replyto_bar').hide();
}

function cancelReply(){
    
    onTweetSuccess();
}

function setReply(id){
    //log('reply:');
    //log(id);
    replyID = id;
    //
    var original = $('#timeline-home #t' + id);
    var otext = '<strong>' + $('.user',original).text() + ":</strong> " + $('.content',original).text()
    //
    $('#replyto_bar').show();
    $('#replyto_bar span').html(otext);
    $("#status").val('@' + $('.user',original).text() + ' ');
    $("#status").focus();
    $("#status")[0].selectionStart = $("#status")[0].selectionEnd = $("#status")[0].value.length;
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

function retweet(id){
    window.connector.retweet(id);
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