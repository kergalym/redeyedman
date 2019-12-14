function ajaxFiles(query_type, attach, urlname) {


         if (attach != null
             && query_type != null
             && urlname != null) {

	         var form = $(attach)[0];
             var formID = new FormData(form);

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                processData: false, // NEEDED, DON'T OMIT THIS
                beforeSend: function() {
                    var percent = '0%';
                    $('.warn_msg').width(percent);
                    $('.warn_msg').css({"display": "block", "background-color": "#4F6988"})
                    $('.warn_msg').html(percent);
                },
                uploadProgress: function(event, position, total, percentComplete) {
                    var percent = percentComplete + '%';
                    $('.warn_msg').width(percent);
                    $('.warn_msg').html(percent);
                },
                complete: function (data) {
                         $('body').html(data.responseText);
                }

            })
        }
}