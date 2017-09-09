//$(document).ready(function() {
//  $('[data-toggle=offcanvas]').click(function() {
//    $('.row-offcanvas').toggleClass(".nav .li a");
//  });
//});

//$(".li a").on("click", function(){
//   $(".li a").find(".active").removeClass("active");
//   $(this).parent().addClass("active");
//});

$(document).ready(function(){
   $('[data-toggle="modal"]').tooltip();
});


$(document).ready(function(){

        // Constructing the suggestion engine
        var data = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace(data),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                url: 'http://localhost:8000/inventory/return_list/?q=%QUERY',
                wildcard: '%QUERY',
            },
        });

        //console.log(data);
        //data.clearPrefetchCache();

        // Initializing the typeahead
        data.initialize();

        $('#product_name').typeahead({
            hint: true,
            highlight: true, /* Enable substring highlighting */
            minLength: 1 /* Specify minimum characters required for showing result */
        },
        {
            name: 'data',
            displayKey: function(data){
                return data;},
            source: data.ttAdapter(),
            limit: Infinity,

        });
    });