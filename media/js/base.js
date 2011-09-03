/* plugins */
(function ($) {
    $.fn.minimenu = function (args) {
        var initials = {
            source: '', // url to get menu
            elements: [], // alternative to former
            element_event: undefined,
            display: 0
        };
        args = $.extend(initials, args);
        return this.each(function () {
            // change display
            var $this = $(this);
            var change_display = function (html, display) {
                $this.html(html).data('id', args.elements[args.display].id);
            }
            change_display(args.elements[args.display].name, args.display);

            // create menu
            var menu = $('<div>').addClass('minimenu-menu'
            ).css({
                display: 'none',  // hide menu at first
                position: 'absolute',
                left: $this.offset().left,
                top: $this.offset().top + $this.height(),
                width: $this.parent().width() - 1
            });


            // fill menu with elements
            $.each(args.elements, function (k, v) {
                // create element
                var element = $('<div>').addClass('minimenu-menu-element'
                ).html(v.name
                ).data('id', v.id
                ).data('seq', k);

                // bind events
                element.click(function () {
                    // run event
                    if (args.element_event) {
                        args.element_event($(this));
                    }
                    // switch with .minimenu
                    $(this).hide();
                    menu.children().each(function () {
                        if ($(this).data('seq') == $this.data('id')) {
                            $(this).show();
                        }
                    });

                    $this.html($(this).html());
                    change_display($(this).html(), $(this).data('seq'));
                });

                // hide if same with display
                if (k == args.display) element.hide();

                // append element to menu
                menu.append(element)
            });
            menu.appendTo('body');

            // click minimenu to show
            $this.click(function () {
                menu.is(':visible')?menu.hide():menu.show();
                return false;
            })
            // click any other part of body to hide
            $('body').click(function (e) {
                menu.is(':visible')&&menu.hide();
                return false;
            });
        });
    }
})(jQuery);

/* components */
var popNoti = function (s) {
    var notiDOM = $('<div>').css({
        'display': 'none',
        'position': 'absolute',
        'height': '30px', 'line-height': '30px',
        'text-align': 'center',
        'top': '20px', 'right': '20px',
    }).append(
        $('<span>').html(s).css({
            'padding': '2px 8px',
            'background': 'red', 'color': '#fff'
        })
    );
    $('body').append(notiDOM);
    notiDOM.fadeIn(300, function () {
        setTimeout(function () {
            notiDOM.fadeOut(300, function () {
                notiDOM.remove();
            })
        }, 500);
    });
}

var new_ajax = function (method) {
    var ajaxObj = {};
    ajaxObj.method = method;
    ajaxObj.url = '';
    ajaxObj.data = {};
    ajaxObj.send = function (succFn) {
        $.ajax({
            type: ajaxObj.method,
            url: ajaxObj.url,
            /*
            headers: {
                'Cookie': 'global_session_id='
            },
            beforeSend: function(jqXHR) {
                var header_cookie_val = 'global_session_id='+api_token;
                jqXHR.setRequestHeader("Cookie", header_cookie_val);
            },
            */
            data: ajaxObj.data,
            success: succFn
        });
    };
    return ajaxObj;
}

var new_steper = function () {
    var steper = {
        steps: [],
        def: function (seq, name, fn) {
            this.steps[seq] = {
                name: name,
                fn: fn
            }
        }
    };
    var show_step = function (seq, name) {
        var monitor = $('#setp_monitor');
        monitor.html('running #' + seq + ': ' + name);
    }
    steper.run = function () {
        $.each(steper.fns, function (k, v) {
            show_step(v.seq, v)
        });
    }
}

var htmlEncode = function (value) { 
  return $('<div>').text(value).html();
}

var htmlDecode = function (value) {
  return $('<div>').html(value).text();
}

/* functions */
var ShowMenu = function () {
    $('#menu').find('.switch').addClass('focus');
    var menu_items = $('#menu').find('li');
    $.each(menu_items, function (i, d) {
        $(d).stop(true, true).delay(i*100).fadeIn(300);
    });
}
var HideMenu = function () {
    $('#menu').find('.switch').removeClass('focus');
    var menu_items = $('#menu').find('li');
    $.each(menu_items, function (i, d) {
        $(d).stop(true, true).delay((menu_items.length - i - 1)*100).fadeOut(300);
    });
}
var ShowCubeditor = function () {
    $('#cubeditor').show(500, function () {
        $('#cubeditor').find('.editor').focus();
    });
}
var HideCubeditor = function () {
    $('#cubeditor').find('.editor').val('');
    $('#cubeditor').hide(500);
}

var SendTask = function () {
    var editor = $('#cubeditor').find('.editor');
    var ajax = new_ajax('POST');
    ajax.url = '/tasks/ajax/create';
    ajax.data = {
        content: editor.val(),
        proj_id: Env.proj_id
    }
    ajax.send(function (resp) {
        popNoti(resp);
        HideCubeditor();
        var path = window.location.pathname;
        (path == '/')?LoadTasks():undefined;
    });
}

/* on ready */
$(function () {

    $('#menu').find('.switch').click(function () {
        var $this = $(this);
        if ($this.hasClass('focus')) {
            HideMenu();
        } else {
            ShowMenu();
        }
    });
    $('#menu li').eq(0).find('a').click(function () {
        HideMenu();
        ShowCubeditor();
        return false;
    });

    $('#cubeditor').find('.editor').bind({
        blur: function () {
            HideCubeditor();
        },
        keydown: function (e) {
            // Ctrl-Enter pressed
            if (e.ctrlKey && e.keyCode == 13) {
                SendTask();
            }
        }
    });
});
