/* global variables */
var Env = {
    task: null,
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
    // hide detail firstly
    HideTaskDetail();

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
            // task dobj is created this place
            var task = $.tmpl(task_tmpl, obj);
            task.data('id', obj.id);
            task.data('status', obj.status);
            if (obj.status) {
                task.addClass('done');
            } else {
                task.addClass('undone');
            }
            task_container.append(task);
            task.delay(i*50).fadeIn(200);
        });
    });
}
var ShowTaskDetail = function (task) {
    var ajax = new_ajax('GET');
    ajax.url = '/tasks/ajax/show?task_id=' + task.data('id');
    ajax.send(function (json) {
        // displays
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
        // events
        var operate = $('#main_right .operate');
        operate.children().show();
        json.status?operate.find('.done').hide():operate.find('.undone').hide();

        // show container
        if (!$('#main_right').is(':visible')) {
            $('#main_right').fadeIn(300);
        }

        // after all change Env.task_id
        Env.task_id = task.data('id');
        Env.task = task;
    });
}
var HideTaskDetail = function () {
    if ($('#main_right').is(':visible')) {
        $('#main_right').fadeOut(300);
    }
}

var HideTask = function () {
    var task = Env.task;
    task.fadeOut(500, function () {
        var gap = $('<li>').addClass('task_item').css('list-style-type', 'none !important');
        task.after(gap);
        gap.animate({
            height: '0px'
        }, 300, function () {
            gap.remove();
        });

        // vary Env attrs
        $(this).remove();
        Env.task = null;
        Env.task_id = null;

        // hide detail endly
        HideTaskDetail();
    });
}
var TaskStatusUpdated = function (st) {
    var task = Env.task;
    if (Env.filter.status != 2) {
        if (st != Env.filter.status) {
            // just hide
            HideTask();
            return
        }
    }

    if (st == 1) {
        task.removeClass('undone').addClass('done');
        $('.operate .done').hide();
        $('.operate .undone').show();
    } else {
        task.removeClass('done').addClass('undone');
        $('.operate .undone').hide();
        $('.operate .done').show();
    }
}

var TaskDone = function () {
    var ajax = new_ajax('POST');
    ajax.url = '/tasks/ajax/done';
    ajax.data = {
        'task_id': Env.task_id
    }
    ajax.send(function (json) {
        TaskStatusUpdated(1);
    });
}
var TaskUndone = function () {
    var ajax = new_ajax('POST');
    ajax.url = '/tasks/ajax/undone';
    ajax.data = {
        'task_id': Env.task_id
    }
    ajax.send(function (json) {
        TaskStatusUpdated(0);
    });
}
var TaskEdit = function () {
    $.jqDialog.prompt(
        'Edit Task',
        Env.task.html(),
        function (content) {
            var ajax = new_ajax('POST');
            ajax.url = '/tasks/ajax/update';
            ajax.data = {
                'task_id': Env.task_id,
                'content': content
            }
            ajax.send(function (json) {
                Env.task.html(json.content);
            });
        }
    );
}
var TaskDelete = function () {
    $.jqDialog.confirm('Delete Task ?',
        function () {
            var ajax = new_ajax('POST');
            ajax.url = '/tasks/ajax/delete';
            ajax.data = {
                'task_id': Env.task_id
            }
            ajax.send(function (json) {
                HideTask();
            });
        }
    );
}

/* on ready */
$(function () {
    // events
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

    var task_items = $('.task_item').live('click', function () {
        if ($(this).hasClass('focus')) {
            $(this).removeClass('focus');
            HideTaskDetail();
        } else {
            $('.task_item').removeClass('focus');
            $(this).addClass('focus');

            ShowTaskDetail($(this));
        }
    });
    var task_operates = $('#main_right .operate a').click(function () {
        var $this = $(this);
        switch ($this.html()) {
            case 'done':
                TaskDone();
                break
            case 'undone':
                TaskUndone();
                break
            case 'edit':
                TaskEdit();
                break
            case 'delete':
                TaskDelete();
                break
        }
        return false;
    });
    var task_comment_editor = $('#task_comment_editor').keydown(function (e) {
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
                ShowTaskDetail(Env.task);
            });
        }
    });


    // running
    LoadContext();
    LoadTasks();

});
