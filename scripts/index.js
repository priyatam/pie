$( function () {
    var index_page_cache = ""
    var app = $.sammy(function() {
        this.element_selector = '#main';
        this.get(rel_path, function (context) {
            if (index_page_cache === "") {
                index_page_cache = $('#main').html()
            }
            context.app.swap(index_page_cache)
        });
        this.get(rel_path + '#/posts/(.*)', function (context) {
            var dhash = document.location.hash;
            post_name = dhash.substring(2);
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === post_name) {
                    break;
                }
            }
            context.app.swap('');
            context.$element().html(data[i]['html'])
        });
    });
    app.run()
});

