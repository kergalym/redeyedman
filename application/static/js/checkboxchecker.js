
$(document).ready(function () {
    $("#checkbox_all").click(function () {
        if ($('#checkbox_all').is(':checked')) {
            $("input[name*='item_chb']").prop('checked', true);
        } else {
            $("input[name*='item_chb']").removeAttr('checked');
        }
    });
    $('input[name="rename"]').click(function () {
    var delid = $('input[name="delid"]').val();
    var item_chb = $("input[name*='item_chb']").val();
    var urlname = '/adminboard/adminboard_main/';

    $.ajax({
        type: "POST",
        url: urlname,
        data: { 
            delid: delid, 
            item_chb: item_chb
        },
        success: function(success) {
        },
        error: function(error) {
        }
        });
        
    });
});