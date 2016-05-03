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

function hideCriterias() {
    // Döljer kriterier efter att man tryckt slumpa på förstasidan
    var centerDiv = document.getElementById("center-div");
    var showstuff = document.getElementById("fullSizeTest")
    
    if (centerDiv.style.display == "block") {
        centerDiv.style.display = "none";
        showstuff.style.display = "none";
        
    }
    else {
        centerDiv.style.display = "none";
        showstuff.style.display = "none";
    }
}


function showCircles() {
    // Döljer kriterier efter att man tryckt slumpa på förstasidan
    var readMore = document.getElementById("readMore");
    var showAll = document.getElementById("showAll");
    readMore.style.display = "block";
    showAll.style.display = "block";
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

// --- FUNKTIONER FÖR FILTRERING AV RESMÅLEN --- //

function randomGrab() {
    // Aktiveras onclick på slumpknapp
    // sparar de valda kriterierna i variabler. Vet inte om vi kan använda detta för att skicka vidare till python sen.
    
    var sendAnythingChoice = document.getElementById('heading1').innerHTML
    var sendAnytimeChoice = document.getElementById('heading3').innerHTML
    var sendAnywhereChoice = document.getElementById('heading2').innerHTML
    
    document.getElementById('fillAnything').value = (sendAnythingChoice);
    document.getElementById('fillAnywhere').value = (sendAnywhereChoice);
    document.getElementById('fillAnytime').value = (sendAnytimeChoice);
        
    var name = document.getElementById('fillAnything').value;
    var name3 = document.getElementById('fillAnywhere').value;
    var name2 = document.getElementById('fillAnytime').value;
    
    localStorage.setItem('fillAnything', name);
    localStorage.setItem('inputTxtTag3', name3);    
    localStorage.setItem('inputTxtTag2', name2);
}



$(document).ready(function() {
    
    
                        $('#send_data').on('click', function() {
                            
                            document.getElementById("center-div").className += " MyClass";
                            
                            var wrap_video = document.getElementById("wrap_video");
                            wrap_video.style.display = "none";
                            
                            
                            $.ajax({
                                url: "/data_post",
                                method: "POST",
                                data: {
                                    data: $('#fillAnything').val() + ' ' + $('#fillAnywhere').val() + ' ' +  $('#fillAnytime').val()
                                },
                                success: function(data) {
                                    console.log(data)
                                    test(data);
                                    
                                }
                            });
                        });
                    });

function test(data1) {
    
$.ajax({
    url: '/getAllWishes',
    type: 'GET',
    success:function(response) {
					
        var data = JSON.parse(response);
        var arr = data1.split(' ');
                      
        if (arr[0] == 'a' || arr[0] == 'the') {
                                        
            var arr_anytime = arr[3];
            var arr_anywhere = arr[2];
            arr = (arr[0] + ' ' + arr[1]);
                                        
            if (arr == 'the ski') {                                            
                
                arr_anytime = arr[4];
                arr_anywhere = arr[3];
                arr = (arr + ' ' + 'slopes');
            }
        } else {
                
            arr_anytime  = arr[2];
            arr_anywhere = arr[1];
            arr = arr[0];
            }
                        
        var counter = "";
                        
        for (var i = 0; i < data.length; i++) {
                            
            if (data[i].Tag.indexOf(arr) >= 0 || arr == 'anything') {
            if (data[i].Tag.indexOf(arr_anywhere) >= 0 || arr_anywhere == 'anywhere') {
            if (data[i].Tag.indexOf(arr_anytime) >= 0 || arr_anytime == 'anytime') {
                            counter += i;
            }
            }
            }
        }
                        
        var newCounter = counter.split('');
        var rand = newCounter[Math.floor(Math.random() * newCounter.length)];

        for (var i = 0; i <= 1; i++) {
                            
            if (data[rand] != undefined) {
            if (data[rand].Tag.indexOf(arr) >= 0 || arr == 'anything') {
            if (data[rand].Tag.indexOf(arr_anywhere) >= 0 || arr_anywhere == 'anywhere') {
            if (data[rand].Tag.indexOf(arr_anytime) >= 0 || arr_anytime == 'anytime') {
                        
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
                $('#picture').append(img);
                            
            }
            }
            }
            } else {
                alert('Det verkar inte finnas några resmål med dessa kriterier. Testa igen.')
            }
        }    
},

error:function(error){
console.log(error);

        }
    });
}