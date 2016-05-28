$(function(){
        
$('#center-div').hide();
$('#bottomLeftDiv').hide();
        
        setTimeout(function() {
          $("#center-div").fadeIn(3000).show()
          $("#bottomLeftDiv").fadeIn(3000).show()
          $('.wrap').fadeOut().hide(8000)
       }, 8000);
        
        $("#typed").typed({
            // strings: ["Typed.js is a <strong>jQuery</strong> plugin.", "It <em>types</em> out sentences.", "And then deletes them.", "Try it out!"],
            stringsElement: $('#typed-strings'),
            typeSpeed: 15,
            backDelay: 500,
            loop: false,
            contentType: 'html', // or text
            // defaults to false for infinite loop
            loopCount: false,
            callback: function(){ foo(); },
            resetCallback: function() { newTyped(); }
        });
                  
        $(".reset").click(function(){
            $("#typed").typed('reset');
        });

    });
        

        
function newTyped(){ /* A new typed object */ }

function foo(){ console.log("Callback"); }