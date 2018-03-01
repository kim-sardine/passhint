$(function () {
    $("#search_name").autocomplete({
        source: "/passhint/autocomplete/",
        autoFocus: true
    });
});

$(function () {
    $('[data-toggle="popover"]').popover()
  })