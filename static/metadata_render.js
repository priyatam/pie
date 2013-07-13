$( function () {
    for (var i =0; i < data.length; i++) {
        title = data[i]['title']
        author =  data[i]['author']
        name =  data[i]['name']
        $('#posts-meta').prepend("<div><a href='#" + name + "'>" + title + "</a></div>");
    }

    $(window).on("hashchange", function (ev) {
        var dhash = document.location.hash;
        console.log(dhash)
        post_name = dhash.substring(1);
        console.log(post_name)
        var html = "";
        for (var i =0; i < data.length; i++) {
            if (data[i]['name'] === post_name) {
                html = data[i]['html']
                break;
            }
        }
        $("#post").html( html );
    });
});
