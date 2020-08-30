(function(document) {
    'use strict';

    let LightTableFilter = (function(Arr) {

        let _input;

        function _onInputEvent(e) {
            _input = e.target;
            let tables = document.getElementsByClassName(_input.getAttribute('data-table'));
            Arr.forEach.call(tables, function(table) {
                Arr.forEach.call(table.tBodies, function(tbody) {
                    Arr.forEach.call(tbody.rows, _filter);
                });
            });
        }

        function _filter(row) {
            let text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
            text = text.replace('ō', 'o');
            text = text.replace('ū', 'u');
            row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
        }

        return {
            init: function() {
                var inputs = document.getElementsByClassName('light-table-filter');
                Arr.forEach.call(inputs, function(input) {
                    input.oninput = _onInputEvent;
                });
            }
        };
    })(Array.prototype);

    document.addEventListener('readystatechange', function() {
        if (document.readyState === 'complete') {
            LightTableFilter.init();
        }
    });

})(document);