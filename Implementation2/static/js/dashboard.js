		$(function(){
			    $.ajax({
        			url: '/getAll',
				type: 'GET',
			        success:function(response) {
					console.log(response);
					var data = JSON.parse(response);
					var itemsPerRow = 0;
					var div = $('<div>').attr('class','row');
					for(var i=0;i<data.length;i++){
						
					    
						if(itemsPerRow<i){
							console.log(i);
							if(i==data.length-1){
								div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Country,data[i].Description,data[i].FilePath,data[i].Tag));
								$('.well').append(div);
							}
							else{
							div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Country,data[i].Description,data[i].FilePath,data[i].Tag));
							itemsPerRow++;
							}
						}
						else{
							$('.well').append(div);
							div = $('<div>').attr('class','row');
							div.append(CreateThumb(data[i].Id,data[i].Title,data[i].Country,data[i].Description,data[i].FilePath,data[i].Tag));
							if(i==data.length-1){
								$('.well').append(div);
							}
							itemsPerRow = 0;
						}
					}
					
			        },
			        error:function(error){
			        	console.log(error);
			        }
    			});

		})
		function CreateThumb(id,title,country,desc,filepath,tag){
			var mainDiv = $('<div>').attr('class','col-sm-3 col-md-3');
			var thumbNail = $('<div>').attr('class','thumbnail');
			var img = $('<img>').attr({'src':filepath,'data-holder-rendered':true,'class':'imgInList'});
           
			var caption = $('<div>').attr('class','caption');
			var title = $('<h3>').text(title);
            var country = $('<p>').text(country);
			var desc = $('<p>').text(desc);
            var tag = $('<p>').text(tag);

			var p = $('<p>');
			var btn = $('<button>').attr({'id':'btn_'+id,'type':'button','class':'btn btn-danger btn-sm'});

			
			
			caption.append(title);
            caption.append(country);
			caption.append(desc);
			caption.append(p);
            
            
			thumbNail.append(img);
			thumbNail.append(caption);
			mainDiv.append(thumbNail);
            caption.append(tag);
			return mainDiv;

			
		}

