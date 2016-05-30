function getAnything(){
   var showAnything = document.getElementById("anything");
    
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

// --- FUNKTIONER FÖR ATT VISA OCH DÖLJA KNAPPAR OCH DIVAR --- //

function showCriterias() {
    // Visar kriterier efter att man tryckt visaknappen
    var centerDiv = document.getElementById("center-div");
    var showstuff = document.getElementById("fullSizeTest")
    var readMoreBox = document.getElementById("readMoresite")
    
    if (centerDiv.style.display == "none") {
        centerDiv.style.display = "block";
        showstuff.style.display = "block";
        readMoreBox.style.display = "none";
    }
    else {
        centerDiv.style.display = "none";
        showstuff.style.display = "none";
        readMoreBox.style.display = "none";
    }
}

function hideFrontPage() {
    
    var readMore = document.getElementById("readMore");
    var showAll = document.getElementById("showAll");    
    var centerDiv = document.getElementById("center-div");
    var showstuff = document.getElementById("fullSizeTest")
    
    // Döljer videon efter första klicket
    var wrap_video = document.getElementById("wrap_video");
    wrap_video.style.display = "none";
    
    // Visar dessa knappar efter att man tryckt slumpa på förstasidan
    readMore.style.display = "block";
    showAll.style.display = "block";
    
    // Döljer kriterier efter att man tryckt slumpa på förstasidan
    if (centerDiv.style.display == "block") {
        centerDiv.style.display = "none";
        showstuff.style.display = "none";
        
    }
    else {
        centerDiv.style.display = "none";
        showstuff.style.display = "none";
    }
    
    //Ändrar opacity för bakgrundsbilden från 0 till 1 vid varje shuffle klick
    document.getElementById('picture').style.opacity = 0;
    
    $('#send_data').attr('disabled', 'disabled');
    setTimeout(enable, 800);
    $('#doneStatus').hide();
    $('#loadingStatus').show();
    
}

function readMoresite() {
    // Visar mer information om resmålet när man trycker på pluset
	var showstuff = document.getElementById("fullSizeTest")
    var readMoreBox = document.getElementById("readMoresite")
    var centerDiv = document.getElementById("center-div");
    
	if (showstuff.style.display == "block") {
        showstuff.style.display = "none";
        readMoreBox.style.display = "none";
        centerDiv.style.display = "none";
   }
   else {
       showstuff.style.display = "block";
       readMoreBox.style.display = "block";
       centerDiv.style.display = "none";
   }
    }

function reloadSite() {
    //aktiveras när man klickar på getaway logotypen. Laddar om sidan och börjar från början.
    location.reload();
}

// --- FUNKTIONER FÖR FADE AV DIVAR--- //

function enable() {
    $('#send_data').removeAttr('disabled');
}

// --- FUNKTIONER FÖR FILTRERING AV RESMÅLEN --- //

function randomGrab() {
    
    // Sparar de tre olika kriterier som är valda i varsin variabel
    var sendAnythingChoice = document.getElementById('heading1').innerHTML
    var sendAnytimeChoice = document.getElementById('heading3').innerHTML
    var sendAnywhereChoice = document.getElementById('heading2').innerHTML
    
    // Sätter in dessa i ett formulär
    document.getElementById('fillAnything').value = (sendAnythingChoice);
    document.getElementById('fillAnywhere').value = (sendAnywhereChoice);
    document.getElementById('fillAnytime').value = (sendAnytimeChoice);
    
    // Sparar detta nya värde i variabler
    var criteria = document.getElementById('heading1').value;
    var criteria2 = document.getElementById('heading2').value;
    var criteria3 = document.getElementById('heading3').value;
    
    // Sparar sedan dessa i localStorage
    localStorage.setItem('fillAnything', criteria);
    localStorage.setItem('fillAnywhere', criteria2);    
    localStorage.setItem('fillAnytime', criteria3);
}

$(document).ready(function() {
    
    // Initialisering av värdet previousRandomNumber som vi använder lite längre ned.
    var previousRandomNumber = 0;
    
    $('#send_data').on('click', function() {
        
        // Hämtar de sparade variablernas värde från localstorage
        var criterias = $('#fillAnything').val() + ' ' + $('#fillAnywhere').val() + ' ' +  $('#fillAnytime').val();
        
        // Hämtar alla resmål
        $.ajax({
            url: '/getAll',
            type: 'GET',
            data: {data: criterias},
            success:function(response) {
                
                var data = JSON.parse(response);

                // Sätter ett mellanrum mellan taggarna (för tydlighet)
                var arr = criterias.split(' ');
                
                
                // Fix för att vissa kriterier har prefix 'a' och 'the'
                if (arr[0] == 'a' || arr[0] == 'the') {
                    
                    var arr_anytime = arr[3];
                    var arr_anywhere = arr[2];
                    arr = (arr[0] + ' ' + arr[1]);
                
                } else {
                    
                    arr_anytime  = arr[2];
                    arr_anywhere = arr[1];
                    arr = arr[0];
                }
                
                // Om kriterier passar överens med en destination sparas dess position i databasen till en variabel.
                // Siffrorna separeras med kommatecken så att man kan separera dem enkelt senare.
                var counter = "";
                
                for (var i = 0; i < data.length; i++) {
                    
                    if (data[i].Tag.indexOf(arr) >= 0 || arr == 'anything') {
                        if (data[i].Tag.indexOf(arr_anywhere) >= 0 || arr_anywhere == 'anywhere') {
                            if (data[i].Tag.indexOf(arr_anytime) >= 0 || arr_anytime == 'anytime') {
                                counter += i + ',';
                                
                            }
                        }
                    }
                }
               
                // Tar bort det sista kommatecknet
                counter = counter.slice(0, -1);

                // Delar upp numren där det finns kommatecken så att inte t.ex. 10 blir 1 och 0.
                var newCounter = counter.split(',');
                
                var rand = newCounter[Math.floor(Math.random() * newCounter.length)];
                    console.log('händer')
                if (data[rand] != undefined) {
               
                // En av positionerna slumpas fram
                do {
                    rand = newCounter[Math.floor(Math.random() * newCounter.length)];
                    /* Kollar om den nya slumpade positionen matchar det som slumpades förra gången */
                    if(rand != previousRandomNumber){
                        
                // Här sätts all information till lämplig div
                // Om ett resmål inte finns, skrivs ett felmeddelande och du återkommer till startsidan.
                    
                    $('#title').empty(); 
                    var title = $('<h1>');
                    title.append(data[rand].Title);
                    $('#title').append(title);

                    var country = $('<p>');
                    country.append(data[rand].Country);
                    $('#title').append(country);

                    $('#readMoresite').empty();     
                    var desc = $('<p>');
                    desc.append(data[rand].Description);
                    $('#readMoresite').append(desc);

                    $('#picture').empty();
                    var img = $('<img>').attr({'src':data[rand].FilePath,'data-holder-rendered':true,});
                    img.append(data[rand].FilePath)
                    $('#picture').append(img).fadeTo( '500' , 1);
                
                    }
                } while (rand == previousRandomNumber)
                    if (counter.length != 2) {
                        
                        /* sätter den slumpade positionen till previousRandomNumber */
                        previousRandomNumber =  rand ;
                    }
                     } else {
                    alert('Det verkar inte finnas några resmål med dessa kriterier. Testa igen.')
                    location.reload();
                    return false;
                }
            },
            error:function(error){
            console.log(error);
            }
        });
    });
});