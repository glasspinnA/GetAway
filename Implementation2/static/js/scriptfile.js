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
    var clickedAnything = document.getElementById(clicked_id).innerHTML;
    document.getElementById('heading1').innerHTML = (clickedAnything);
}

function grabAnywhereHtml(clicked_id){
    var clickedAnywhere = document.getElementById(clicked_id).innerHTML;
    document.getElementById('heading2').innerHTML = (clickedAnywhere);
}

function grabAnytimeHtml(clicked_id){
    var clickedAnytime = document.getElementById(clicked_id).innerHTML;
    document.getElementById('heading3').innerHTML = (clickedAnytime);
}


function randomGrab() {
    // Aktiveras onclick på slumpknapp
    // sparar de valda kriterierna i variabler. Vet inte om vi kan använda detta för att skicka vidare till python sen.
    var sendAnythingChoice = document.getElementById('heading1').innerHTML
    var sendAnytimeChoice = document.getElementById('heading3').innerHTML
    var sendAnywhereChoice = document.getElementById('heading2').innerHTML
    
    document.getElementById('fillAnything').value = (sendAnythingChoice);
    document.getElementById('fillAnytime').value = (sendAnytimeChoice);
    document.getElementById('fillAnywhere').value = (sendAnywhereChoice);
        
    var name = document.getElementById('fillAnything').value;
    var name2 = document.getElementById('fillAnytime').value;
    var name3 = document.getElementById('fillAnywhere').value;
    
    localStorage.setItem('inputTxtTag', name);
    localStorage.setItem('inputTxtTag2', name2);
    localStorage.setItem('inputTxtTag3', name3);

    console.log (fillAnything)


    
}
function randomAgain(){
        
    var name = localStorage.getItem('inputTxtTag');
    var name2 = localStorage.getItem('inputTxtTag2');
    var name3 = localStorage.getItem('inputTxtTag3');

    console.log(name,name2,name3);
    
    document.getElementById('fillAnything').value = (name);
    document.getElementById('fillAnytime').value = (name2);
    document.getElementById('fillAnywhere').value = (name3);
        
		
	}
