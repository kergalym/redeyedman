var formData = new FormData($('form')[0]);
$.ajax({
      type: "POST",
      processData: false,
      contentType: false,
      url: "/app/Helpers/Helper_fileManager.php",
      data:  formData 
      })
      .done(function( data ) {
            $('#warn_msg').addClass('alert alert-warning warn_msg').css({"background-color": '#9A2F2F', "color": "white"});
            $('#warn_msg').alert("Файл(ы) загружен(ы)");
            console.log(data);           
      });
