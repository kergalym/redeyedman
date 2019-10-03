/*!
 * Made Simple CMS (Alpha) v0.1
 * Copyright Galym Kerimbekov <email dot com>
 * Licensed under GPL v2
 */

$(document).ready(function () {
        $("#upload_submit").click(function (e) {
           e.preventDefault();
            admMsg('warn_msg', '#9A2F2F', 'POST', '/app/Helpers/Helper_fileManager');
        });
});

function admMsg(warn_msg, colortype, query_type, urlname) {

    var formData = new FormData();
    formData.append('button f-upload', $('input[type=file]')[0].files[0]);
    
        $.ajax({
            type: query_type,
            url: urlname,
            data: formData,
            cache: false,
            processData: false, // Don't process the files
            contentType: false, // Set content type to false as jQuery will tell the server its a query string request
            success: function (formData) {
                $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
                $('#' + warn_msg).html(formData.responseText); 
                console.log(formData);
            }
        })
        .fail(function (formData) {
            $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
            $('#' + warn_msg).html(formData.responseText);
            console.log(formData);
        });
}

