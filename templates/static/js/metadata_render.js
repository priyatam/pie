$( function () {
for (var i =0; i < metadata.length; i++) {
  title = metadata[i]['title']
  author =  metadata[i]['author']
  name =  metadata[i]['_name']
  
  $('#notes-meta').prepend("<div><a href='#" + name + "'>" + title + "</a></div>");
}

$(window).on("hashchange", function (ev) {
  var dhash = document.location.hash;
  var e = $("[data-id='" + dhash + "']")
  console.log(dhash)
  $(".note").each(function (e) { $(this).css({display: "none"}) });
  e.css({display: "block"});
});



});
