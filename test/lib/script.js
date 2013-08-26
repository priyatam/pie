$( function () {

    var relative_path = window.location.pathname;

    var app = $.sammy(function() {
        this.element_selector = '#main';

        this.get(relative_path, function (context) {
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === config.first_page) {
                    break;
                }
            }
            context.app.swap(data[i]['html'])
        });

        this.get(relative_path + '#' + '/(.*)', function (context) {
            var dhash = document.location.hash;
            post_name = dhash.substring(2);
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === post_name) {
                    break;
                }
            }
            context.app.swap(data[i]['html'])
        });

    });

    app.run()
});

