$(function () {

    $('.citation').each(function() {
//        if $(this).data('content')
        $(this).attr({
//         if page #
            'data-toggle': "popover",
            'href': '#' + $(this).data('content').split(" ")[0].toLowerCase()
        });
    });

    $('[data-toggle="popover"]').popover({
    animation: true, html: true, placement: 'auto', trigger: 'hover', delay: {show: 500, hide: 1500},
    template: '<diass="popovv cler" role="tooltip"><div class="arrow"></div> \
                    <h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    });

});