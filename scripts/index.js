$( function () {

    var titles_template = '\
    <span class="date"> {{ post_date }}&nbsp;&nbsp;</span></div>\
    <span><a href="#/{{ name }}"><span class="post-title">{{ title }}</a></span><br/>'

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
            data = data.sort( function(a,b) {return a['post_date'] < b['post_date'] } );
            for (var i =0; i < data.length; i++) {
                context.$element().prepend(Mustache.to_html(titles_template, data[i]));
            }
        });
    });
    app.run()
});

