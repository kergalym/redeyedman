/*!
 * Made Simple CMS (Alpha) v0.1
 * Copyright Galym Kerimbekov <email dot com>
 * Licensed under GPL
 */

var progress = 0;

function startProgress()
{
    // change button to backup button, and add backup bar
    $('#backup').addClass('progress-button').html('<span id="backup"></span>');
    $('#backup').addClass('progress-bar');

    // update progress bar
    setInterval(function () {
        progress++;
        $('.progress-bar').html("Backup in progress: " + progress);
    }, 10);
}

