$( function () {

    var get_dict = function (key, dict, def) {
        if (key in dict) {
            if (dict[key] != null || dict[key] != undefined) {
                return dict[key]
            }
        }
        return def
    }

    var app = $.sammy("#wrapper", function() {

        this.post("#/search", function (context) {
            var query = new RegExp(this.params['query'], "i")
            var results = []
            for (var i =0; i < data.length; i++) {
                    console.log(data[i])
                    if (get_dict('title', data[i], '-1').search(query) != -1 || get_dict('author', data[i], '-1').search(query) != -1) {
                        results.push(i)
                }
            }
            var html = ""
            for (var i =0; i < results.length; i++) {
                html += "<a href='#/" + data[results[i]]['name'] + "'>" + data[results[i]]['title'] + "</a><br/>"
            }
            $("#main").html(html)

            /*Re-run Syntax Highlighters*/
            /*$('pre code').each(function(i, e) {hljs.highlightBlock(e)});*/
            return false;
        });

        this.get('#/(.*)', function (context) {
            var dhash = document.location.hash;
            post_name = dhash.substring(2);
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === post_name) {
                    break;
                }
            }
            $("#main").html(data[i]['html'])
            /*Re-run Syntax Highlighters*/
            /*$('pre code').each(function(i, e) {hljs.highlightBlock(e)});*/
        });

        this.get("" , function (context) {
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === config.first_page) {
                    break;
                }
            }
            $("#main").html(data[i]['html'])
            /*Re-run Syntax Highlighters*/
            /*$('pre code').each(function(i, e) {hljs.highlightBlock(e)});*/
        });

    });

    app.run()
});

