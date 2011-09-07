
$(function () {
    var in_projs = $('.box a').click(function () {
        /*
        var ajax = new_ajax('POST');
        ajax.url = '/context';
        ajax.data = {
            proj_id: $(this).attr('value')
        }
        ajax.send();
        */
        $.cookie('context_proj_id', $(this).attr('value'));
        document.location.href = '/';
    });
});
