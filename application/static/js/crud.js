/* 
 * Copyright (C) 2018 Galym Kerimbekov <kegalym2@mail.ru>
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

function ajaxFiles(warn_msg, colortype, query_type, attach, urlname) {
	    
	    var form = $(attach)[0];
        var formID = new FormData(form);
        var redirect = "".concat("<a id='redirect' href='",  $(location).attr('href'), "'>", "Reload the page", "</a>");

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                processData: false, // NEEDED, DON'T OMIT THIS
                statusCode: {
                    200: function (data) {
                        $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
                        $('#' + warn_msg).html("".concat(data, " ", redirect));
                    }
                }

            })

}

function ajaxPost(warn_msg, colortype, query_type, form, urlname, btnAct) {

	    var rawForm = $(form).serialize();
        var btnName = btnAct + '=' + btnAct + '&';
        var formID = btnName + rawForm;
        var redirect = "".concat("<a id='redirect' href='",  $(location).attr('href'), "'>", "Reload the page", "</a>");

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
         		dataType: 'json',
		        encode: true,
                statusCode: {
                    200: function (data) {
                        $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
                        $('#' + warn_msg).html("".concat(data.responseText, " ", redirect));
                    }
                }

            })

}

function gfxConv(warn_msg, colortype, query_type, form, urlname, btnAct, chkBtn, qrangeField, qrange, imgpathField, imgpath, pict) {

        var rawForm = $(form).serialize();
        var btnSubmit = btnAct + '=' + btnAct + '&';
        var btnChBox = chkBtn + '=' + pict + '&';
        var addressBar = imgpathField + '=' + imgpath + '&';
        var qrange = qrangeField + '=' + qrange + '&';
        var formID = addressBar + qrange + btnChBox + btnSubmit + rawForm;

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                dataType: 'json',
                encode: true,
                statusCode: {
                    200: function (data) {
                        $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
                        $('#' + warn_msg).html("".concat(data.responseText, " ", redirect));
                    }
            }

        })

}    

function pubSwitch(warn_msg, colortype, query_type, form, urlname, btnAct, chkBtn, content, radioField, radio) {

        var rawForm = $(form).serialize();
        var btnSubmit = btnAct + '=' + btnAct + '&';
        var btnChBox = 'content=' + chkBtn + '&';
        var contentField = "content_index";
        var content = contentField + '=' + content + '&';
        var radio = radioField + '=' + radio + '&';
        var formID = content + radio + btnChBox + btnSubmit + rawForm;
        var redirect = "".concat("<a id='redirect' href='",  $(location).attr('href'), "'>", "Reload the page", "</a>");

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                dataType: 'json',
                encode: true,
                statusCode: {
                    200: function (data) {
                        $('#' + warn_msg).addClass('alert alert-warning warn_msg').css({"background-color": colortype, "color": "white"});
                        $('#' + warn_msg).html("".concat(data.responseText, " ", redirect));
                    }
            }

        })

}    


$(document).ready(function () {
    
    // MULTIPLE RECORDS MANAGEMENT IN THE DASHBOARD
    // var isChecked must be checked for int or null in the future

     $( "#checkbox_all" ).click(function(){
             if ($('#checkbox_all').is(':checked')) {
                    $("input[name*='item_chb']").prop('checked', true);	 
             } else {
                    $("input[name*='item_chb']").removeAttr('checked');
             }
    });

    // VARIOUS DASHBOARD ACTIONS

    var currentpage = $(location).attr('pathname');

    if (currentpage == '/adminboard/adminboard_main') {

        $('#rename').click(function (rev) {
            rev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_main', btnAct);
        });
        $('#delete').click(function (dev) {
            dev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_main', btnAct);
        });


        // PUB SWITCHER BLOCK
        $("input[name*=item_chb]").click(function () {

           var chkBtn = '';
           var radioField = 'radio';
           var isChecked = 0;
            
           if (this.checked) {

                content = $(this).attr("value");
                chkBtn = content;
                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');

                $("input[type*=radio]").on('change', function () {
                    radio = $(this).val();

                });    

                $('#pub_submit').click(function (pub) {
                    pub.preventDefault();
                    var btnAct = $(this).attr('id');
                  
                    pubSwitch('warn_msg', '#9A2F2F', 'POST', '#pubswitch', 
                            '/adminboard/adminboard_main', 
                            btnAct, chkBtn, content, radioField, radio
                            );
                });
           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }    

        });    



    } else if (currentpage == '/adminboard/adminboard_inner') {

        $('#rename').click(function (rev) {
            rev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_inner', btnAct);
        });
        $('#delete').click(function (dev) {
            dev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_inner', btnAct);
        });


        // PUB SWITCHER BLOCK
        $("input[name*=item_chb]").click(function () {

           var chkBtn = '';
           var radioField = 'radio';
           var isChecked = 0;
            
           if (this.checked) {

                content = $(this).attr("value");
                chkBtn = content;
                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');

                $("input[type*=radio]").on('change', function () {
                    radio = $(this).val();
                    console.log(radio = $(this).val());

                });    

                $('#pub_submit').click(function (pub) {
                    pub.preventDefault();
                    var btnAct = $(this).attr('id');
                  
                    pubSwitch('warn_msg', '#9A2F2F', 'POST', '#pubswitch', 
                            '/adminboard/adminboard_inner', 
                            btnAct, chkBtn, content, radioField, radio
                            );
                });
           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }    

        });    

    } else if (currentpage == '/adminboard/adminboard_category') {
    
        $('#rename').click(function (rev) {
            rev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_category', btnAct);
        });
        $('#delete').click(function (dev) {
            dev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_op', '/adminboard/adminboard_category', btnAct);
        });
    
    } else if (currentpage == '/adminboard/adminboard_media') {

        // ADMINBOARD FILE CRUD BLOCK
        $('#upload_submit').click(function (upev) {
            upev.preventDefault();
            ajaxFiles('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_media');
        });
        $('#mkdir-submit').click(function (mkev) {
            mkev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_media', btnAct);
        });
        $('#rename').click(function (rev) {
            rev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_media', btnAct);
        });
        $('#delete').click(function (dev) {
            dev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_media', btnAct);
        });


        // GFX CONVERTER BLOCK
        $("input[name*=item_chb]").click(function () {

           var imgpathField = '';
           var imgpath = '';
           var chkBtn = '';
           var pict = '';
           var qrangeField = 'qrange';
           var qrange = '50';
           var isChecked = 0;
            
           if (this.checked) {

                imgpathField = $("input[name*=addressbar]").attr("name");
                imgpath = $("input[name*=addressbar]").attr("value");
                pict = $(this).attr("value");
                chkBtn = 'item_chb';
                isChecked = 1;

                $('#gfxconv_active').css('display', 'block');
                $('#gfxconv').css('display', 'block');

                $("input[id*=qrange]").on('change', function () {
                    qrange = $(this).val();
                    $('#qval').text(qrange + "%");

                });    

                $('#conv_submit').click(function (conv) {
                    conv.preventDefault();
                    var btnAct = $(this).attr('id');
                  
                    gfxConv('warn_msg', '#9A2F2F', 'POST', '#gfxconv', 
                            '../../Helpers/Helper_fileManager_gfxconv', 
                            btnAct, chkBtn, qrangeField, qrange, 
                            imgpathField, imgpath, pict
                            );
                });
           } else {

                $('#gfxconv_active').css('display', 'none');
                $('#gfxconv').css('display', 'none');
           }    

        });    



        // ADMINBOARD IMAGEVIEW BLOCK
        $('#table-striped [href]').click(function (item) {
            $(this).data('clicked', true);
            item.preventDefault();
            var str = $(this).attr("href");
            var pattern = /.png|.jpg|.jpe|.jpe|.gif|.svg|.json|.ico/;
            if (pattern.test(str) == false) {
               // We have directory then
               $("input[name='addressbar']").val(str);
            }
        });

        // ADMINBOARD SHOW BLOCK


    } else if (currentpage == '/adminboard/adminboard_users') {

        $('#adduser_active').css('display', 'block');
        $('#adduser').css('display', 'block');

        $('#rename').click(function (rev) {
            rev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_users', btnAct);
        });
        $('#delete').click(function (dev) {
            dev.preventDefault();
            var btnAct = $(this).attr('id');
            ajaxPost('warn_msg', '#9A2F2F', 'POST', '#form_upload', '/adminboard/adminboard_users', btnAct);
        });

    } else {

        $('#adduser_active').css('display', 'none');
        $('#adduser').css('display', 'none');
    }    

});
