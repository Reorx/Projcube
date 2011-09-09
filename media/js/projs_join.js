var JoinProj = function (obj) {
    $.jqDialog.prompt(
        'send with words',
        '',
        function (words) {
            alert(words)
        }
    );
}

$(function () {
    var join_input = $('input[name="name"]').keydown(function (e) {
        if (e.keyCode == 13) {
            JoinProj(join_input);
        }
    });
    join_bt = $('input[type="submit"]').click(function () {
        if (!join_input.val()) return false;
        JoinProj(join_input);
        return false;
    })
    var projs = $('.proj.box .item span').click(function () {
        join_input.val($(this).html()).focus();
    });
});
