function getBotResponse() {
    var rawText = $("#textInput").val();
    var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
    $.get("/get", { msg: rawText }).done(function(data) {
        var botHtml = '<p class="botText"><span>' + data + '</span></p>';
        $("#chatbox").append(botHtml);
        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
}

$("#textInput").keypress(function(e) {
    if (e.which == 13) {
        getBotResponse();
    }
});

$("#buttonInput").click(function() {
    getBotResponse();
});

function startVoiceRecognition() {
    var recognition = new webkitSpeechRecognition();
    recognition.onresult = function(event) {
        var text = event.results[0][0].transcript;
        $("#textInput").val(text);
        getBotResponse();
    }
    recognition.start();
}
