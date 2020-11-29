$(function () {

    $('.citation').each(function() {
        let data_content = $(this).data('content');
        if (RegExp(/\w+ \d+/i).test(data_content)) {
            href = data_content.split(" ")[0].toLowerCase();
        }
        else { href = ''; }
        $(this).attr({'data-toggle': "popover", 'href': '#' + href});
    });

    $('[data-toggle="popover"]').popover({
    animation: true, html: true, placement: 'auto', trigger: 'hover', delay: {show: 500, hide: 1500},
    template: '<div class="popover" role="tooltip"><div class="arrow"></div> \
                    <h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    });

});
