$( function () {

    var app = $.sammy("#wrapper", function() {

        this.post("#/search", function (context) {
            var query = new RegExp(this.params['query'], "i")
            var results = []
            for (var i =0; i < data.length; i++) {
                if (data[i]['_type'] !== 'dynamic') {
                    if (data[i]['title'].search(query) != -1 || data[i]['author'].search(query) != -1) {
                        results.push(i)
                    }
                }
            }

            var html = ""
            for (var i =0; i < results.length; i++) {
                html += "<a href='#/" + data[results[i]]['name'] + "'>" + data[results[i]]['title'] + "</a><br/>"
            }
            $("#main").html(html)
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
        });

        this.get("" , function (context) {
            for (var i =0; i < data.length; i++) {
                if (data[i]['name'] === config.first_page) {
                    break;
                }
            }
            $("#main").html(data[i]['html'])
        });

    });

    app.run()
});

