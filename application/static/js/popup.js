$(function () {

    $('.citation').each(function() {
        $(this).attr({
            'data-toggle': "popover",
            'href': '#' + $(this).data('content').split(" ")[0].toLowerCase()
        });
    });

    $('[data-toggle="popover"]').popover({
    animation: true, html: true, placement: 'auto', trigger: 'hover', delay: {show: 500, hide: 1500},
    template: '<div class="popover" role="tooltip"><div class="arrow"></div> \
                    <h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    });

});