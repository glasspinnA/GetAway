function getAnything(){
    var showAnything = document.getElementById("anything");
    console.log(showAnything.style.display);
    if (showAnything.style.display == "block") {
        showAnything.style.display = "none";
    }
    else {
        showAnything.style.display = "block";
    }
     }

function getAnywhere(){
    var showAnything = document.getElementById("anywhere");
    if (showAnything.style.display == "block") {
        showAnything.style.display = "none";
    }
    else {
        showAnything.style.display = "block";
    }
     }

function getAnytime(){
    var showAnything = document.getElementById("anytime");
    if (showAnything.style.display == "block") {
        showAnything.style.display = "none";
    }
    else {
        showAnything.style.display = "block";
    }
     }


function grabAnythingHtml(clicked_id){
    	document.getElementById('heading1').innerHTML = (clicked_id); { 
            getAnything()}
}

function grabAnywhereHtml(clicked_id){
    	document.getElementById('heading2').innerHTML = (clicked_id); { 
            getAnywhere()}
}

function grabAnytimeHtml(clicked_id){
    	document.getElementById('heading3').innerHTML = (clicked_id); {
            getAnytime()}
}


function randomGrab() {
    // Aktiveras onclick på slumpknapp
    // sparar de valda kriterierna i variabler. Vet inte om vi kan använda detta för att skicka vidare till python sen.
    var sendAnythingChoice = document.getElementById('heading1').innerHTML
    var sendAnywhereChoice = document.getElementById('heading2').innerHTML
    var sendAnytimeChoice = document.getElementById('heading3').innerHTML
    var allChoices = [sendAnythingChoice, sendAnywhereChoice, sendAnytimeChoice]
    
    document.getElementById('fillAnything').value = (sendAnythingChoice);
    var fillAnything =  document.getElementById('fillAnything').value
    alert (fillAnything);
    console.log (fillAnything)
}


    
