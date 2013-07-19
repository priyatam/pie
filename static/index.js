$( function () {
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
            for (var i =0; i < data.length; i++) {
                title = data[i]['title']
                author =  data[i]['author']
                name =  data[i]['name']
                context.app.swap('');
                context.$element().prepend("<div><a href='#/" + name + "'><h2>" + title + "</h2></a></div>");
            }
        });
    });
    app.run()
});

