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
    $('input[name="query"]').on('input', function() {
        $('input[name="query"]').on('keypress', function(e) {
          if(e.keyCode === 13) {
            e.preventDefault();
          }
        });
        if (!this.value) {
            $('.table.table-striped').css({
                "display": "inline-table"
            });
            $('#table-striped-search').css({
                "display": "none"
            });
        } else {                                           
            $.ajax({
                url: $(location).attr("href"),
                data: $('#formsearch').serialize(),
                type: 'POST',
                success: function (data) {
                    console.log($(location).attr("href"));
                    $('.table.table-striped').css({
                        "display": "none"
                    });
                    $('#table-striped-search').css({
                        "display": "inline-table"
                    });
                    
                    if (typeof data === "object") {
                        
                        for (var i = 0; i < 1; ++i) {
                           var inputvarID = data.id;
                           var inputvarUser = data.login;
                           var inputvarEmail = data.email;
                           var inputvarDate = data.date;                                   
                           var divs = "".concat(
                                '<tr>',
                                    '<td>', inputvarID, '</a></td>',
                                    "<td><a href='/adminboard/editpage_id_users/", inputvarID, "' title='Редактировать пользователя'>", inputvarTitle, "</a></td>",
                                    '<td>', inputvarAuthor, '</a></td>',
                                    '<td>', inputvarCategory, '</a></td>',
                                    '<td>', inputvarDate, '</a></td>',
                                    "<td><input type='text' id='delid_", inputvarID,
                                        "' name='delid_", inputvarID, "' value='", inputvarID, "' size='1' ></td>",
                                    "<td><input type='checkbox' id='checkbox' name='item_chb' value='",
                                        inputvarID, "' /></td>",
                                '</tr>',
                           )    

                            $('#table-striped-search').append(divs);
                        }   
                    } else {
                        return false;
                    }  
                },
                error: function (error) {
                    return error;
                }
            });
        } 
    });
});
