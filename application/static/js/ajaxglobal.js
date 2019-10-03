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
    $('#cddir').on('click', function(e) {
	e.preventDefault();
	var form = $('#formnav').serialize()
	var xpath = $(location).attr('href')
	var custom_path = '/adminboard/adminboard_media'

	if (typeof form != "object") {
	   xpath = custom_path;
	}

	$.ajax({
	url: xpath,
	data: form,
	dataType: "json",
	type: 'POST',
	  success: function(data) {
        if (typeof data === "object") {
            $('addressbar').text(data.addressbar);
            
            for (var i = 0; i < 1; ++i) {
               var fileID = data.id;
               var fileRPath = data.relpath;
               var fileName = data.name;
               var fileOwner = data.owner;
               var fileSize = data.size;
               var filePerm = data.perm;
               var fileDate = data.date;                                   
               var divs = '<tr>';
                divs += '<td>' + fileID + '</a></td>';
                divs += "<td><a href='" + fileRPath + "' title='"
                    + fileName + "'><img src='" 
                    + fileName + "'> <style='border-style:solid; border-width:1px; height:32px; width:32px'>" 
                    + fileName + "</a></td>";
                divs += '<td>' + fileOwner + '</a></td>';
                divs += '<td>' + fileSize + '</a></td>';
                divs += '<td>' + filePerm + '</a></td>';
                divs += '<td>' + fileDate + '</a></td>';
                divs += "<td><input type='text' id='delid_" + fileID
                        + "' name='delid_" + fileID + "' value='" + fileID 
                        + "' size='1' ></td>";
                divs += "<td><input type='checkbox' id='checkbox' name='item_chb' value='"
                        + fileID + "' /></td>";
                divs += '</tr>';   

                $('#table-striped').append(divs);
            }   
        } else {
            return false;
        }  
          
	  },
	  error: function (error) {
	    console.log(error);
          }

	    });
    });
});
