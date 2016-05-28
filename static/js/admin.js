		$(function(){
			    $('#fileupload').fileupload({
        			url: 'upload',
        			dataType: 'json',
        			add: function (e, data) {
        				data.submit();
        			},
			        success:function(response,status) {
					console.log(response.filename);
					var filePath = 'static/Uploads/' + response.filename;
					$('#imgUpload').attr('src',filePath);
					$('#filePath').val(filePath);
			        	console.log('success');
			        },
			        error:function(error){
			        	console.log(error);
			        }
    			});
		})

	$(function(){
		
		GetDestinations(1);
		$('#btnUpdate').click(function(){
			$.ajax({
			url : '/update',
			data : {title:$('#editTitle').val(),country:$('#editCountry').val(),description:$('#editDescription').val(),id:localStorage.getItem('editId'),filePath:$('#imgUpload').attr('src'),tag:$('#editTag').val()},
			type : 'POST',
			success: function(res){
				

			$('#editModal').modal('hide');
							    
				GetDestinations(1);
				
				

				
			},
			error: function(error){
				console.log(error);
			}
		});
		});

		$('document').on('click','.navigation li a',function(){
			console.log('me in');
		});
	});

	function GetDestinations(_page){
		
		$.ajax({
			url : '/getAll',
            type : 'GET',
			success: function(res){
				
				var wishObj = JSON.parse(res);
				
                console.log(wishObj);
                
                $('#ulist').empty();
                
                for(var i=0;i<wishObj.length;i++){
                $('#listTemplate').tmpl(wishObj[i]).appendTo('#ulist');
                }
				

			},
			error: function(error){
				console.log(error);
			}
		});
	}

	function ConfirmDelete(elem){
		localStorage.setItem('deleteId',$(elem).attr('data-id'));
		$('#deleteModal').modal();
	}

	function Delete(){
		$.ajax({
			url : '/delete',
			data : {id:localStorage.getItem('deleteId')},
			type : 'POST',
			success: function(res){
				var result = JSON.parse(res);
				if(result.status == 'OK'){
					$('#deleteModal').modal('hide');
					GetDestinations();
				}
				else{
					alert(result.status);	
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	}

	function Edit(elm){
		localStorage.setItem('editId',$(elm).attr('data-id'));
        
		$.ajax({
			url : '/getById',
			data : {id:$(elm).attr('data-id')},
            type : 'POST',
			success: function(res){
				
				var data = JSON.parse(res);
                
                $('#editTitle').val(data[0]['Title']);
                $('#editCountry').val(data[0]['Country']);
				$('#editDescription').val(data[0]['Description']);
				$('#imgUpload').attr('src',data[0]['FilePath']);
				$('#editTag').val(data[0]['Tag']);
                $('#editModal').modal();
				
			},
			error: function(error){
				console.log(error);
			}
		});
	}