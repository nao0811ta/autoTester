$('body').on('click', '*', function(event) {
    //window.alert(' ID of element- testing');
    console.log(event);
    console.log('nao');
    //window.alert(' ID of element=' + $(this).attr('id'));  // Get ID attribute
    //window.alert(' ID of Parent element=' + $(this).parent().attr('id'));
});

var event = document.createEvent("MouseEvents");
event.initMouseEvent("click", true, true, window,
    0, 0, 0, 0, 0,
    false, false, false, false,
    0, null);
/*
chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.executeScript(null,{file:'jquery-3.1.1.js',allFrames:true});
	chrome.tabs.executeScript(null,{file:'script.js',allFrames:true});
});
*/
