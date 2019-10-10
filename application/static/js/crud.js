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

function ajaxPost(query_type, form, urlname, actBtn, addressBar, csrf_token) {

         if (form != null
             && urlname != null
             && query_type != null
             && actBtn != null
             && addressBar != null
             && csrf_token != null) {

             var actBtn = actBtn + '=True' + '&';
             var addressBar = 'addressbar=' + addressBar + '&';
             var csrf_token = 'csrf_token=' + csrf_token + '&';
             var formID = addressBar + form + actBtn + csrf_token;
             var cls_warn = null;

             $.ajax({
                 type: query_type,
                 url: urlname,
                 data: formID,
          		 dataType: 'json',
  	             encode: true,
  	             cache: false,
                 complete: function (data) {
                         $('body').html(data.responseText);
                 }

             })
          }

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

function formElemIdentify(urlname, event) {

            var multiple = null;

            var actBtn = null;

            if ($(event).attr('id') === 'rename') {
                actBtn = $(event).attr('id');
            }

            if ($(event).attr('id') === 'delete') {
                actBtn = $(event).attr('id');
            }

            var addressBar = $('input[name="addressbar"]').attr('value');
            var csrf_token = $('input[name="csrf_token"]').attr('value');

            var id = null;
            var i_num = null;
            var d_num = null;
            var form = null;
            var d_array = $('input[name="delid"]');
            var ch_array = $('input[name=item_chb]:checked');

            if (ch_array.length === 1) {
                multiple = 0;
            } else if (ch_array.length > 1) {
                multiple = 1;
            }

            if (multiple === 0) {

                id = ch_array.attr('id');
                d_num = d_array.attr( "id" );

                i_num = id.replace( /^\D+/g, '');
                d_num = d_num.replace( /^\D+/g, '');
                i_str = $('input[name=item_chb]:checked').attr('value');

                $.each(d_array, function(k, v) {

                    d_num = v.id.replace( /^\D+/g, '')

                    if (d_num === i_num) {
                        i_str = 'item_chb=' + i_str + '&';
                        d_str = 'delid=' + v.value + '&';
                        form = i_str + d_str;
                        ajaxPost('POST', form, urlname, actBtn, addressBar, csrf_token);
                    }
                });

            } else if (multiple === 1) {

                id = ch_array.attr('id');
                d_num = d_array.attr( "id" );

                var equal = 0;

                if (d_array.length === ch_array.length) {
                    equal = 1;
                }

                i_num = id.replace( /^\D+/g, '');
                d_num = d_num.replace( /^\D+/g, '');
                i_str = $(this).attr('value');


                if (equal === 1) {

                   var zip = (ch, d) => ch.map((x,i) => [x,d[i]]);

                   $.each(zip(ch_array, d_array), function(d, ch) {
                       i_num = ch.id.replace( /^\D+/g, '');
                       d_num = d.id.replace( /^\D+/g, '');

                       if (d_num === i_num) {
                           i_str = 'item_chb=' + ch.value + '&';
                           d_str = 'delid=' + d.value + '&';
                           form = i_str + d_str;
                           ajaxPost('POST', form, urlname, actBtn, addressBar, csrf_token);
                       }

                   });

                   var zip = (ch, d) => ch.map((x,i) => [x,d[i]]);
                   // for a, b in zip(list1, list2):
                   for (let [ch, d] of zip(ch_array, d_array))
                   //     print(a + b)
                        console.log(d + ' : ' + ch);

                }

            }
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

    if (currentpage == '/adminboard/adminboard_main/') {

        $('#rename').click(function (rev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                rev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });

        $('#delete').click(function (dev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                dev.preventDefault();
                formElemIdentify(currentpage, this);
            }
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
                            '/adminboard/adminboard_main/',
                            btnAct, chkBtn, content, radioField, radio
                            );
                });

           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }    

        });

    } else if (currentpage == '/adminboard/adminboard_inner/') {

        $('#rename').click(function (rev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                rev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });
        $('#delete').click(function (dev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                dev.preventDefault();
                formElemIdentify(currentpage, this);
            }
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
                            '/adminboard/adminboard_inner/',
                            btnAct, chkBtn, content, radioField, radio
                            );
                });
           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }    

        });    

    } else if (currentpage == '/adminboard/adminboard_category/') {
    
        $('#rename').click(function (rev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                rev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });

        $('#delete').click(function (dev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                dev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });
    
    } else if (currentpage == '/adminboard/adminboard_media/') {

        // ADMINBOARD FILE CRUD BLOCK
        $('#upload_submit').click(function (upev) {
            upev.preventDefault();
            ajaxFiles('warn_msg', '#9A2F2F', 'POST', '#formnav', '/adminboard/adminboard_media/');
        });

        $('#mkdir-submit').click(function (mkev) {
            mkev.preventDefault();
            formElemIdentify(currentpage, this);
        });

        $('#rename').click(function (rev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                rev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });

        $('#delete').click(function (dev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                dev.preventDefault();
                formElemIdentify(currentpage, this);
            }
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
                            '/adminboard/adminboard_media/',
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


    } else if (currentpage == '/adminboard/adminboard_users/') {

        $('#adduser_active').css('display', 'block');
        $('#adduser').css('display', 'block');

        $('#rename').click(function (rev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                rev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });

        $('#delete').click(function (dev) {
            if ($('input[name=item_chb]:checked').length === 1) {
                dev.preventDefault();
                formElemIdentify(currentpage, this);
            }
        });

    } else {

        $('#adduser_active').css('display', 'none');
        $('#adduser').css('display', 'none');
    }    

});
