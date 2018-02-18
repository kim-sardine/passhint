$(function () {
    $("#search_name").autocomplete({
        source: "/passhint/autocomplete/",
        autoFocus: true
    });
});