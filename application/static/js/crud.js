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

function ajaxPost(query_type, urlname, actBtn, csrf_token, form) {

         if (urlname != null
             && query_type != null
             && actBtn != null
             && csrf_token != null
             && form != null) {

             var actBtn = actBtn + '=True' + '&';
             var item_chb = 'item_chb=' + item_chb + '&';
             var delid = 'delid=' + delid + '&';
             var csrf_token = 'csrf_token=' + csrf_token + '&';
             var formID = form + actBtn + csrf_token;
             console.log(formID);
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

function addUser(query_type, form, urlname, actBtn, csrf_token) {

         if (form != null
             && urlname != null
             && query_type != null
             && actBtn != null
             && csrf_token != null) {

             var actBtn = actBtn + '=True' + '&';
             var rawForm = $(form).serialize();;
             var csrf_token = 'csrf_token=' + csrf_token + '&';
             var formID = actBtn + csrf_token + rawForm;

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


function gfxConv(query_type, form, urlname, btnAct, chkBtn, qrangeField, qrange, imgpathField, imgpath, pict, csrf_token) {

        var rawForm = $(form).serialize();
        var btnSubmit = btnAct + '=True' + '&';
        var btnChBox = chkBtn + '=' + pict + '&';
        var addressBar = imgpathField + '=' + imgpath + '&';
        var qrange = qrangeField + '=' + qrange + '&';
        var csrf_token = 'csrf_token=' + csrf_token + '&';
        var formID = addressBar + qrange + btnChBox + btnSubmit + csrf_token + rawForm;

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                dataType: 'json',
                encode: true,
                 complete: function (data) {
                         $('body').html(data.responseText);
                 }

            })

}    

function getImgSize(query_type, form, urlname, btnAct, chkBtn, qrangeField, qrange, imgpathField, imgpath, pict, csrf_token) {

        var rawForm = $(form).serialize();
        var btnSubmit = btnAct + '=True' + '&';
        var btnChBox = chkBtn + '=' + pict + '&';
        var addressBar = imgpathField + '=' + imgpath + '&';
        var qrange = qrangeField + '=' + qrange + '&';
        var csrf_token = 'csrf_token=' + csrf_token + '&';
        var formID = addressBar + qrange + btnChBox + btnSubmit + csrf_token + rawForm;

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                complete: function (data) {
                        if (pict.slice((pict.length)-3, ) != 'svg') {
                            var data_array = JSON.parse(data.responseText);
                            $('#width').attr('value', data_array['width']);
                            $('#height').attr('value', data_array['height']);
                        }

                 }

            })

}

function pubSwitch(query_type, urlname, btnAct, chkBtn, radio, csrf_token) {

        var btnSubmit = btnAct + '=True' + '&';
        var btnChBox = 'item_chb=' + chkBtn + '&';
        var radio = 'published=' + radio + '&';
        var token = 'csrf_token=' + csrf_token + '&';
        var formID = radio + btnChBox + btnSubmit + token;

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                dataType: 'json',
                encode: true,
                 complete: function (data) {
                         $('body').html(data.responseText);
                 }

            })

}    

function pubMultSwitch(query_type, urlname, btnAct, chkBtn, radio, csrf_token) {

        var btnSubmit = btnAct + '=True' + '&';
        var radio = 'published=' + radio + '&';
        var token = 'csrf_token=' + csrf_token + '&';
        var btnChBox = '';

        $.each(chkBtn, function(i) {
                btnChBox += 'item_chb=' + chkBtn[i].value + '&';
        });

        var formID = radio + btnChBox + btnSubmit + token;

            $.ajax({
                type: query_type,
                url: urlname,
                data: formID,
                dataType: 'json',
                encode: true,
                 complete: function (data) {
                         $('body').html(data.responseText);
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

            if ($(event).attr('id') === 'user_submit') {
                actBtn = $(event).attr('id');
                var csrf_token = $('input[name="csrf_token"]').attr('value');
                addUser('POST', '#adduser', '/adminboard/useradd', actBtn, csrf_token);
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
                        form = i_str + d_str + 'addressbar=' + addressBar + '&';
                        console.log(form);
                        ajaxPost('POST', urlname, actBtn, csrf_token, form);
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
                           ajaxPost('POST', urlname, actBtn, csrf_token, form);
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
           var radio = null;
           var isChecked = 0;
            
           if (this.checked) {

                chkBtn = $(this).val();
                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');
                $('input[name="pub_off"]').attr( "checked", true );
                $('input[name="pub_on"]').attr( "checked", false );

                $('input[name="pub_on"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_main',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                });

                $('input[name="pub_off"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_main',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                });

                if ($('input[name="pub_on"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_main',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                }

                if ($('input[name="pub_off"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_main',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                }


           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }    

        });

        // PUB MULTIPLE SWITCHER BLOCK
        $("input[name*=items_chb]").click(function () {

           var chkBtn = $("input[name*=item_chb]").serializeArray()

           var radio = null;
           var isChecked = 0;

           if (this.checked) {

                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');
                $('input[name="pub_off"]').attr( "checked", true );
                $('input[name="pub_on"]').attr( "checked", false );

                $('input[name="pub_on"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_main',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                });

                $('input[name="pub_off"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_main',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                });

                if ($('input[name="pub_on"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_main',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                }

                if ($('input[name="pub_off"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_main',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                }


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
           var radio = null;
           var isChecked = 0;

           if (this.checked) {

                chkBtn = $(this).val();
                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');
                $('input[name="pub_off"]').attr( "checked", true );
                $('input[name="pub_on"]').attr( "checked", false );

                $('input[name="pub_on"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_inner',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                });

                $('input[name="pub_off"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_inner',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                });

                if ($('input[name="pub_on"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_inner',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                }

                if ($('input[name="pub_off"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubSwitch('POST','/adminboard/pub_switcher_inner',
                                 btnAct, chkBtn, radio, csrf_token
                                 );
                     });

                }


           } else {

                $('#pubswitch_active').css('display', 'none');
                $('#pubswitch').css('display', 'none');
           }

        });

        // PUB MULTIPLE SWITCHER BLOCK
        $("input[name*=items_chb]").click(function () {

           var chkBtn = $("input[name*=item_chb]").serializeArray()

           var radio = null;
           var isChecked = 0;

           if (this.checked) {

                isChecked = 1;

                $('#pubswitch_active').css('display', 'block');
                $('#pubswitch').css('display', 'block');
                $('input[name="pub_off"]').attr( "checked", true );
                $('input[name="pub_on"]').attr( "checked", false );

                $('input[name="pub_on"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_inner',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                });

                $('input[name="pub_off"]').click(function () {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_inner',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                });

                if ($('input[name="pub_on"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_off"]').attr( "checked", false );
                    radio = $(this).val();

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_inner',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                }

                if ($('input[name="pub_off"]').is(':checked')) {
                    $(this).attr( "checked", true );
                    $('input[name="pub_on"]').attr( "checked", false );
                    radio = 0;

                     $('#pub_submit').click(function (pub) {
                         pub.preventDefault();
                         var btnAct = $(this).attr('id');
                         var csrf_token = $('input[name="csrf_token"]').val();

                         pubMultSwitch('POST','/adminboard/pub_switcher_inner',
                                        btnAct, chkBtn, radio, csrf_token
                                      );
                     });

                }


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
           var csrf_token = null;
           var dict = null;

           if (this.checked) {

                imgpathField = $("input[name*=addressbar]").attr("name");
                imgpath = $("input[name*=addressbar]").attr("value");
                csrf_token = $('input[name="csrf_token"]').attr("value");
                pict = $(this).attr("value");
                chkBtn = 'item_chb';
                chkBtnValue = $(this).attr('value');
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
                  
                    gfxConv('POST', '#gfxconv',
                            '/adminboard/gfx_converter',
                            btnAct, chkBtn, qrangeField, qrange, 
                            imgpathField, imgpath, pict, csrf_token
                            );
                });

                $('#measure_submit').click(function (meas) {
                    meas.preventDefault();
                    var btnAct = $(this).attr('id');

                    getImgSize('POST', '#gfxconv',
                               '/adminboard/gfx_converter',
                               btnAct, chkBtn, qrangeField, qrange,
                               imgpathField, imgpath, pict, csrf_token
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


    } else if (currentpage == '/adminboard/adminboard_filemanager/') {

        // ADMINBOARD FILE CRUD BLOCK
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

        // ADMINBOARD ADDUSER BLOCK
        $('#user_submit').click(function (dev) {
           dev.preventDefault();
           formElemIdentify(currentpage, this);
        });

    } else {

        $('#adduser_active').css('display', 'none');
        $('#adduser').css('display', 'none');
    }

});
