/*!
 * Made Simple CMS (Alpha) v0.1
 * Copyright Galym Kerimbekov <email dot com>
 * Licensed under GPL v2
 */

$(document).ready(function () {
    $('submit').click(function (e) {
                $('#warn_msg').addClass('alert alert-warning warn_msg').css({"background-color": "#9A2F2F", "color": "white"});
                $('#warn_msg').html('lol');
                console.log();
            });

});


