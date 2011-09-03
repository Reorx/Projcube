
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

$(function () {


    // 
    $('#minimenu-sendtype').minimenu({
        elements: [
            {name: 'task', id: 0},
            {name: 'note', id: 1},
            {name: 'msg', id: 2}
        ]
    });

    // get minimenu-proj elements
    var GetProjs = function () {
        var ajax = new_ajax('GET');
        ajax.url = '/projs/ajax'
        ajax.send(function (json) {
            var elmts = []
            $.each(json, function (i, obj) {
                elmts[i] = {name: obj.name, id: obj.id};
            });
            $('#minimenu-proj').minimenu({
                elements: elmts
            });
        })
    }
    GetProjs();

    // task input submit
    $('#inplat-textarea').keydown(function (e) {
        // Ctrl-Enter pressed
        if (e.ctrlKey && e.keyCode == 13) {
            var options = {
                sendtype: $('#minimenu-sendtype').data('id'),
                proj: $('#minimenu-proj').data('id')
            }

            var ajax = new_ajax('POST');
            switch (options.sendtype) {
                case 0: // task
                    ajax.url = '/tasks/ajax/create';
                    ajax.data = {
                        content: $(this).val(),
                        proj_id: $('#minimenu-proj').data('id')
                    }
                    ajax.send(function (resp) {
                        popNoti(resp);
                        $('#task_input').val('').blur();
                    });
                    break
                case 1: // note
                    break
                case 2: // msg
                    break
                default:
                    break
            }
        }
    });

    //
    var ReloadColumn = function (json) {
        var tasks_container = $('#readboard-column-left').find('.items');
        tasks_container.empty();
        var task_tmpl = '<div class="item">' +
                            '<div class="info">' +
                                '<span>#${id}</span>' +
                                '<span>${time_delta}</span>' +
                            '</div>' +
                            '<div class="content">${content}</div>' +
                            '<div class="clearfix"></div>' +
                        '</div>';
        $.each(json, function (i, obj) {
            $.tmpl(task_tmpl, obj).appendTo(tasks_container);
        });
    };

    $('#minimenu-filter').minimenu({
        elements: [
            {name: 'all', id: 0},
            {name: 'my', id: 1},
            {name: 'others', id: 2}
        ],
        element_event: function (elmt) {
            var ajax = new_ajax('GET');
            ajax.url = '/tasks/ajax?proj_id=' + $.cookie('context_proj_id') +
                       '&mode=' + elmt.data('id');
            ajax.send(function (json) {
                ReloadColumn(json);
            });
        }
    });

});
