/* Designed by: */
/* Galym Kerimbekov kegalym2 AT mail.ru */
/* especially for Made Simple CMS */
/* ======================================= */

/* PORTRAIT MEDIA QUERY EVENT */


$(document).ready(function () {
    $("button").click(function () {
        if ($("button").attr("aria-expanded")) {
            var id = document.getElementById('main');
            var top = 300;
            id.setAttribute("style", "margin-top: " + top.toString() + "px");

        } else {
            var id = document.getElementById('main');
            id.getAttribute("style");
            id.removeAttribute("style");
        }
    });
});


function ariaHandler()
{
    document.getElementById("main").click();
    if ($("button").attr("aria-expanded", true)) {
        var id = document.getElementById("main");
        console.log(id);
        var top = 300;
        id.setAttribute("style", "margin-top:" + top.toString() + "px");
        console.log(id);

    } else {
        id.getAttribute("style");
        console.log(id);
        id.removeAttribute("style");
        console.log(id);

    }
}
/*
 var shrt_text = document.getElementById("short_text").div.innerHTML.substring(0, 700);
 var text = shrt_text.substring(0, 700);
 return text;
 */
