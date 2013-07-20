$( function () {

    var titles_template = '\
    <div><a href="#/{{ name }}"><span class="post-title">{{ title }}</span></a>\
    <span class="date"> ( {{ modified_date }} )</span></div>'

    var app = $.sammy(function() {
        this.element_selector = '#main';
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
        this.get(rel_path, function(context) {
            context.app.swap('');
            for (var i =0; i < data.length; i++) {
                context.$element().prepend(Mustache.to_html(titles_template, data[i]));
            }
        });
    });
    app.run()
});

