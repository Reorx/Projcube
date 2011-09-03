
    /* static switchers */
    $('body').click(function (e) {
        var s = $('.selector_trigger.static').next();
        //if (!$(e.target).is('.selector_trigger.static')) {
        if (s.is(':visible')) {
            s.hide();
        }
        //}
    });
    $('.selector_trigger.static').click(function () {
        //alert('x');
        //$('#tasks_filter_selector').show();
        //$('.selector.static').show();
        var s = $(this).next();
        if (!s.is(':visible')) {
            s.width($(this).parent().width()).show();
        }
        return false;
    });


    /* dynamic switchers ? */
    /*
     * function (callbefore, callafter) {
     *    callbefore;
     *    *main*
     *    callafter;
     * }
    */
    // proj
    $('#proj_selector_trigger').click(function () {
        var ajax = new_ajax();
        ajax.url = '/proj/projects/ajax?is_creator=0';
        ajax.method = 'GET';
        ajax.send(function (json) {
            var proj_selector = $('#proj_selector');
            var current_id = $('#proj_selector_trigger').attr('nmval');
            proj_selector.empty(
            ).width($('#proj_selector_trigger').parent().width()-1
            ).show();
            /*
            if (json.id != current_id) {
            }
            */
            $.each(json, function (i, obj) {
                if (obj.id != current_id) {
                var proj_dom = $('<li>').html(obj.name
                    ).addClass('fui-tiny_clearly'
                    ).attr('nmval',obj.id
                    );
                    proj_selector.append(proj_dom);
                }
            });
        });
        return false;
    });

    $('#proj_selector').find('li').live('click', function () {
        //alert($(this).html());
        var t = $('#proj_selector_trigger');
        t.html($(this).html());
        t.attr('nmval', $(this).attr('nmval'));
        $(this).parent().hide();
    });


    var SelectorTriggerCallback = function (obj) {
        obj.parent().hide();
    }


    // task filter selector
    $('#tasks_filter_selector').find('li').live('click', function () {
        var ajax = new_ajax();
        ajax.method = 'GET';
        ajax.url = '/proj/tasks/ajax?proj_id='
        + $('#current_context').attr('nmval')
        + '&mode=' + $(this).attr('nmval');
        ajax.send(function (json) {
            ReloadTasks(json);
        });

        // generate now_filter from pre_filter
        var pre_filter = $('#tasks_filter');
        var now_filter = $('<li>').addClass('fui-tiny_clearly'
        ).html(pre_filter.html()).attr('nmval', pre_filter.attr('nmval'));
        // add after clicked
        $(this).after(now_filter);
        // change pre_filter display
        pre_filter.html($(this).html()).attr('nmval', $(this).attr('nmval'));
        // remove clicked node
        $(this).remove();
        // hide parent
        $('#tasks_filter_selector').hide();
    });

