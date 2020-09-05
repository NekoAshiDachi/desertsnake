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

// NEW REFERENCE FORM ==================================================================================================

let options = document.querySelectorAll('#training_add_source option');
for (let o of options) {
    o.onclick = function() {

        // hide add_source options
        for (let o of options) {
            document.getElementById('training_' + o.textContent.toLowerCase()).classList.add('d-none');
        }
        document.querySelector('#training_style_org').classList.add('d-none');

        // show selected add_source option and textarea
        document.getElementById('training_' + o.textContent.toLowerCase()).classList.remove('d-none');
        document.querySelector('#training_text').classList.remove('d-none');

        // exceptions
        switch (o.textContent) {
            case 'Video':
                document.querySelector('#training_style_org').classList.remove('d-none');
                document.querySelector('#training_person').classList.remove('d-none');

                // remove placeholder allowing form validation and replace with input placeholders
                document.querySelector('#video_id').value = '';
                document.querySelector('#video_id').placeholder = '11-character ID after "v="';
                document.querySelector('#video_name').value = '';
                document.querySelector('#video_name').placeholder = 'Video name';
        }
        console.log('Form errors: {{ form.errors }}');
    }
}

// clear training form text field and set defaults
document.querySelector('#add_src_btn').onclick = function() {
    document.querySelector('#training_add_source').selectedIndex = 3;
    document.querySelector('#category').selectedIndex = 0;
    document.querySelector('#person').selectedIndex = 0;
    document.querySelector('#style').selectedIndex = 1;
    document.querySelector('#org').selectedIndex = 0;

    document.querySelector('#training_textarea').placeholder = 'Description';
    document.querySelector('#training_textarea').value = '';
};