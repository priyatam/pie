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
            console.log(data.length)
            context.app.swap('');
            for (var i =0; i <= data.length; i++) {
                title = data[i]['title']
                author =  data[i]['author']
                name =  data[i]['name']
                mtime =  data[i]['modified_date']
                console
                // this should be a template
                context.$element().prepend("<div><a href='#/" + name + "'><span class='post-title'>" + title + "</span></a>"
                                           + "<span class='date'> ( " + mtime +  " )</span></div>");
            }
        });
    });
    app.run()
});

