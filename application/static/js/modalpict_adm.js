/* 
 * Copyright (C) 2017 Galym Kerimbekov <kegalym2@mail.ru>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

$(document).ready(function() {
    $('#table-striped [href]').click(function(event) {
        event.preventDefault();
        var imgurl = $(this).attr("href");
        var pattern = /.png|.jpg|.jpe|.jpe|.gif|.svg|.json|.ico/;
        if (pattern.test(imgurl) == true) {
		// Change these vars only!!
		var body_item = '#adm_sidebar';
		var z_int = '4';
		var center_img = "margin-left: auto; margin-right: auto";
		// Change these vars only!!
		
		/*  Predefined div strings */
		var imgovr_div = "<div id='img-ovr' class='img-ovr' align='center'> </div>";
		var imgshow_div = "".concat("<div id='imgshow' class='imgshow'>",
		    "<div id='img-plus'> | + | </div><div id='img-minus'> | - | ", 
            "</div><div id='img-close'> | X | </div>", 
            "</div>");
		var reconst_imgurl = "".concat("<img src=", imgurl, " style='border-style:",
		    "solid; border-width:5px;margin:5px;", center_img, ";'>");
			
		// Add an image overlay at the end of the block 
		$(body_item).prepend(imgovr_div);
		$('.img-ovr').css({"background-color": "black", "width": "100%", 
		    "height": "100%", "z-index": z_int, "position": "fixed", 
		    "opacity": "0.2"})
			       .animate({opacity: 0.9, top: '0%'}, 200);
		
		// Append an image overlay first
		$('#img-ovr').append(imgshow_div);

		// Define an image properties
		$('.imgshow').css({"background": "black", "width": "95%", 
		    "height": "100%", "z-index": "5", "margin-left": "1%", 
		    "margin-top": "10%"})
			       .animate({opacity: 1, top: '50%'}, 200);

		// Define the close button properties
		$('#img-close').css({"color": "white", "width": "40px", 
		    "height": "40px", "cursor": "pointer", "margin-left": "94%"});

		// Define the plus button properties
		$('#img-plus').css({"color": "white", "width": "40px",
		    "height": "40px", "cursor": "pointer", "margin-left": "90%"});
		
		// Define the minus button properties
		$('#img-minus').css({"color": "white", "width": "40px",
		    "height": "40px", "cursor": "pointer", "margin-left": "92%"});

		// Append an image 
		$('#imgshow').append(reconst_imgurl);
		$('#img-ovr').css({"overflow": "scroll"})
		$('#img-ovr').scroll();

		// Get an image dimensions
		var p = 10;
		var width = 95;
		var low = 30;
		var more = 95;
	    
		// Minimize an image
		$('#img-minus').click(function() {
		    if ( width <= low) {
			 $('#img-minus').css({"color": "gray"});
			 return false;
		     } else {
			 width -= p;                 
			 $('#img-plus').css({"color": "white"}); 
			 $('#imgshow img').attr({'width': width + '%'});                     
		     } 
		});
		
		// Maximize an image            
		$('#img-plus').click(function() {
		    if (width >= more) {
			 $('#img-plus').css({"color": "gray"});
			 $('#imgshow img').attr({'width': '95%'});
			 return false;
		     } else {
			 width += p;                 
			 $('#img-minus').css({"color": "white"}); 
			 $('#imgshow img').attr({'width': width + '%'});                     
		     }   
		});
		
		// Disable an image overlay by click
		$('#img-close').click(function() {
		    $('#img-ovr').css('background-color', 'black')
		       .animate({opacity: 0, top: '45%'}, 200,
		       function() {
			$(this).css('display', 'none');
			$('#img-ovr').fadeOut(400);
			$('#content_bottom_b').removeClass('.imgshow');
		       }              
		    );  
		});
        }
    });
});
