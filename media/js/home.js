/* global variables */
var Env = {
    task_id: null,
    proj_id: $.cookie('context_proj_id'),
    filter: {
        people: 'me',
        status: 0
    }
};

/* functions */
var LoadContext = function () {
    var ajax = new_ajax('GET');
    ajax.url = '/projs/ajax/show?proj_id=' + Env.proj_id;
    ajax.send(function (json) {
        $('#proj-name').hide().html(json.name).fadeIn(500);
    });
}
var LoadTasks = function () {
    var params = {
        proj_id: Env.proj_id
    }
    params = $.extend(params, Env.filter);
    var ajax = new_ajax('GET');
    ajax.url = '/tasks/ajax?' + $.param(params);
    ajax.send(function (json) {
        var task_container = $('#tasks').empty();
        var task_tmpl = '<li class="task_item" style="display: none;">${content}</li>';
        $.each(json, function (i, obj) {
            var task = $.tmpl(task_tmpl, obj);
            task.data('id', obj.id);
            task_container.append(task);
            task.delay(i*50).fadeIn(200);
        });
    });
}
var ShowTaskDetail = function (id) {
    var ajax = new_ajax('GET');
    ajax.url = '/tasks/ajax/show?task_id=' + id;
    ajax.send(function (json) {
        $('#task_info').find('.creator').html(json.creator.username);
        $('#task_info').find('.time').html(json.created_time);
        $('#task_comments').empty();
        comment_tmpl = '<div class="item">' +
                            '<div class="content"></div>' +
                            '<div class="info">' +
                                '<a href="/user/${creator.id}">${creator.username}</a>' +
                                '<span>${created_time_simple}</span>' +
                            '</div>' +
                        '</div>'
        $.each(json.comments, function (i, obj) {
            var comment = $.tmpl(comment_tmpl, obj);
            comment.find('.content').html(obj.content);
            $('#task_comments').append(comment);
        });

        if (!$('#main_right').is(':visible')) {
            $('#main_right').fadeIn(300);
        }

        // after all change Env.task_id
        Env.task_id = id
    });
}

/* on ready */
$(function () {
    // events
    $('.task_item').live('click', function () {
        if ($(this).hasClass('focus')) {
            $(this).removeClass('focus');
            $('#main_right').fadeOut(300);
        } else {
            $('.task_item').removeClass('focus');
            $(this).addClass('focus');

            ShowTaskDetail($(this).data('id'));
        }
    });

    $('#task_comment_editor').keydown(function (e) {
        var $this = $(this);
        // Ctrl-Enter pressed
        if (e.ctrlKey && e.keyCode == 13) {
            var ajax = new_ajax('POST');
            ajax.url = '/tasks/ajax/commenton';
            ajax.data = {
                task_id: Env.task_id,
                content: $(this).val()
            }
            ajax.send(function (json) {
                $this.val('').blur();
                popNoti(json.msg);
                ShowTaskDetail(Env.task_id);
            });
        }
    });

    $('#proj-options .people').find('a').click(function () {
        Env.filter.people = $(this).attr('data');
    });
    $('#proj-options .status').find('a').click(function () {
        Env.filter.status = $(this).attr('data');
    });
    $('#proj-options').find('a').click(function () {
        if (!$(this).hasClass('active')) {
            $(this).parent().children().removeClass('active');
            $(this).addClass('active');
            LoadTasks();
        }
        return false;
    });


    // running
    LoadContext();
    LoadTasks();

});
