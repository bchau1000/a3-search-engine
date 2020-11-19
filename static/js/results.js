const query_string = window.location.search.substr(1);

function populate_page(response)
{
    var search_tokens = query_string.substr(6).replace('+', ' ')
    $('#results_header').append("'" + search_tokens + "'")

    // Parse the JSON array from response, list out the urls
    for(let i = 0; i < response.length; i++)
        $('#url_table').append('<a href="' + response[i]['url'] + '"> ' + response[i]['url'] + '</a>' + '<br>');
}

$(document).ready(function(){
    // Grab the query from the url, send a request to api/results
    // Should return a response in the form of a JSON array
    $.ajax({
        url: 'api/results',
        data: query_string,
        type: 'GET',
        success: function(response){
            console.log(response);
            populate_page(response)
        },
        error: function(error){
            console.log(error);
        }
    });
});