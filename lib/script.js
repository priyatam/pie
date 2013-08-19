$( function () {

    var relative_path = window.location.pathname;

    var titles_template = '\
        <span class="date"> {{ post_date }}&nbsp;&nbsp;</span>\
        <span><a href="#/blog/{{ name }}"><span class="post-title">{{ title }}</a></span><br/>'

    function load_pages(context, type) {
        context.app.swap('');
        data = data.sort( function(a,b) {return a['post_date'] < b['post_date'] } );
        var html = ""
        for (var i =0; i < data.length; i++) {
            html += Mustache.to_html(titles_template, data[i])
        }
        context.$element().prepend( "<div class='post-titles'>" + html + "</div>")
    }

    var app = $.sammy(function() {
        this.element_selector = '#main';
        this.get(relative_path, function (context) {
            if (config.first_page === "blog") {
                load_pages(context, "blog")
            }
            else {
                for (var i =0; i < data.length; i++) {
                    if (data[i]['name'] === config.first_page) {
                        break;
                    }
                }
                context.app.swap(data[i]['html'])
            }
        });
        this.get(relative_path + '#/page' + '/(.*)', function (context) {
            var dhash = document.location.hash;
            post_name = dhash.substring(7);
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === post_name) {
                    break;
                }
            }
            context.app.swap('');
            context.$element().html(data[i]['html'])
        });
         this.get(relative_path + '#/blog', function (context) {
            load_pages(context, "blog")
        });
        this.get(relative_path + '#/blog' + '/(.*)', function (context) {
            var dhash = document.location.hash;
            post_name = dhash.substring(7);
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

