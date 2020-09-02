// clear modal body on click
for (let element of document.querySelectorAll('.modal_custom_trigger')) {
    element.onclick = function() {
        let modal_custom_body = document.querySelector('#modal_custom_body');
        while (modal_custom_body.firstChild)
            modal_custom_body.removeChild(modal_custom_body.firstChild);
    };
}

// TODO make switch case across different media types
$(function () {

    // should add option if youtube ID not passed
    $('.modal_youtube').on('click', function() {
        $(this).attr({'data-toggle': 'modal', 'data-target': '#modal_custom'});
        var youtube_link = 'https://www.youtube.com/embed/' + $(this).data('youtube_id');

        $('<iframe src=' + youtube_link + ' width="100%" height="500" frameborder="0" \
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> \
            </iframe>').appendTo('#modal_custom_body');
    });

    $('.modal_img').on('click', function() {
        $(this).attr({'data-toggle': 'modal', 'data-target': '#modal_custom'});
        var img_link = 'https://drive.google.com/uc?id=' + $(this).data('src');

        $('<img src=' + img_link + " style='width: 100%;'>").appendTo('.modal-body');
        $('<small>(' + $(this).data('citation') + ')</small>').appendTo('.modal-body');
    });
});

for (let trigger of document.querySelectorAll('.modal_map_trigger')) {
    trigger.onclick = function() {

        let modal_map_header = document.querySelector('#mapLabel');
        modal_map_header.textContent = trigger.textContent;

        let modal_map_body_iframe = document.querySelector('#modal_map_body iframe');

        let iframe_query = 'https://www.google.com/maps/embed/v1/place?';
        let api_key = 'key=AIzaSyCf0d44n0cyl9N1yYUyFlVekitvU86GwJc';  // TODO hide api_key
        let data_map_id = trigger.getAttribute('data-map-id');
        let new_query = iframe_query + api_key + '&q=place_id:' + data_map_id;

        modal_map_body_iframe.setAttribute('src', new_query);
    }
}

