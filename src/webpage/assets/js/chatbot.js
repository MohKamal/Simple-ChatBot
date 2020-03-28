$(document).ready(function() {
    //Sending default hi
    sendRequest('Hi');
    //init var
    var sending = false;
    //Sending event for the user
    $("#human_message").on('keyup', function(e) {
        if (e.keyCode === 13) {
            sendText();
        }
    });
    //Sending event for the user
    $("#btnSend").on('click', function() {
        sendText();
    });

    //verifying the input value and if the user 
    //have sended already a request before sending a new one
    function sendText() {
        if (sending) {
            addWaitPlease();
            return 0;
        }
        message = $("#human_message").val();
        $("#human_message").val('');
        // is empty
        if (message.length <= 0)
            return 0;
        // is empty or whitespace
        if (!message.trim())
            return 0;
        sendRequest(message);
    }

    //Sending request
    function sendRequest(message) {
        //Getting current time to display the user message
        var dt = new Date();
        var time = dt.getHours() + ":" + dt.getMinutes();
        var myMsg = `
            <div class="outgoing_msg">
                <div class="sent_msg">
                    <p>${message}</p>
                    <span class="time_date"> ${time}   |    Today</span> </div>
            </div>`;
        //dispalying user message
        $(".msg_history").append(myMsg);
        //diplaying typing animation
        addTyping();
        sending = true;
        //Sending the request
        $.ajax({
            type: "POST",
            url: "/chatbot.py",
            data: { 'human_message': message },
            dataType: 'html',
            success: function(html) {
                //Getting the bot anwser and time
                var $text = $(html).filter(function() { return $(this).is('p') });
                var $time = $(html).filter(function() { return $(this).is('span') });
                var msg = `
            <div class="incoming_msg">
                <div class="incoming_msg_img"> <img src="assets/images/user-profile.png" alt="sunil"> </div>
                <div class="received_msg">
                    <div class="received_withd_msg">
                        <p>${$text.text()}</p>
                        <span class="time_date"> ${$time.text()}    |    Today</span></div>
                </div>
            </div>`;
                //removing typing animation
                console.log('removing');
                removeTyping();
                //We remove wait please messages if there is some
                removeWaitPlease();
                //displaying bot message
                $(".msg_history").append(msg);
                sending = false;
                //Scrolling
                scrollToConversationEnd();
            },
            error: function(request, ajaxOptions, thrownError) {
                //When the server return error
                sending = false;
                //We remove typing animation
                removeTyping();
                //We remove wait please messages if there is some
                removeWaitPlease();
                //And displaying error on box (alert)
                alert(request.responseText);
            }

        });
        scrollToConversationEnd();
    }

    //Adding tyoping animation
    function addTyping() {
        var typing = `<div class="incoming_msg typing">
                        <div class="incoming_msg_img"> <img src="assets/images/user-profile.png" alt="sunil"> </div>
                        <div class="received_msg">
                            <div class="is-typing">
                                <div class="jump1"></div>
                                <div class="jump2"></div>
                                <div class="jump3"></div>
                                <div class="jump4"></div>
                                <div class="jump5"></div>
                            </div>
                        </div>
                    </div>`;
        $(".msg_history").append(typing);
    }
    //remove typing animation
    function removeTyping() {
        console.log('removed');
        $('.typing').remove();
    }

    //Adding wait message
    function addWaitPlease() {
        var dt = new Date();
        var time = dt.getHours() + ":" + dt.getMinutes();
        var wait = `
        <div class="incoming_msg wait">
            <div class="incoming_msg_img"> <img src="assets/images/user-profile.png" alt="sunil"> </div>
            <div class="received_msg">
                <div class="received_withd_msg">
                    <p>I'm trying to anwser, wait please!</p>
                    <span class="time_date"> ${time}    |    Today</span></div>
            </div>
        </div>`;
        $(".msg_history").append(wait);
        scrollToConversationEnd();
    }

    //remove wait message
    function removeWaitPlease() {
        $('.wait').remove();
    }

    //Auto scroll to bottom
    function scrollToConversationEnd() {
        var div = $('.msg_history');
        $('.scrollbit').bind('scroll mousedown wheel DOMMouseScroll mousewheel keyup', function(evt) {
            if (evt.type === 'DOMMouseScroll' || evt.type === 'keyup' || evt.type === 'mousewheel') {

            }
            if (evt.originalEvent.detail < 0 || (evt.originalEvent.wheelDelta && evt.originalEvent.wheelDelta > 0)) {
                clearInterval(scrollbit);
            }
            if (evt.originalEvent.detail > 0 || (evt.originalEvent.wheelDelta && evt.originalEvent.wheelDelta < 0)) {
                clearInterval(scrollbit);
            }
        });

        var scrollbit = setInterval(function() {
            var pos = div.scrollTop();
            if ((div.scrollTop() + div.innerHeight()) >= div[0].scrollHeight) {
                clearInterval(scrollbit);
            }
            div.scrollTop(pos + 1);
        }, 0);
    };

});