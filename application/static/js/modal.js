$(function () {

    // should add option if youtube ID not passed
    $('.modal_youtube').on('click', function() {
        $(this).attr({'data-toggle': 'modal', 'data-target': '#modal_custom'});
        var youtube_link = 'https://www.youtube.com/embed/' + $(this).data('youtube_id');

        $('#modal_custom_body').empty();

        $('<iframe src=' + youtube_link + ' width="100%" height="500" frameborder="0" \
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> \
            </iframe>').appendTo('#modal_custom_body');
    });

    $('.modal_img').on('click', function() {
        $(this).attr({'data-toggle': 'modal', 'data-target': '#modal_custom'});
        var img_link = 'https://drive.google.com/uc?id=' + $(this).data('src');

        $('.modal-body').empty();

        $('<img src=' + img_link + " style='width: 100%;'>").appendTo('.modal-body');
        $('<small>(' + $(this).data('citation') + ')</small>').appendTo('.modal-body');
    });
});
