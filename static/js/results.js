// Grab the query entered in the search bar from the url
const query_string = window.location.search.substr(1);

function populate_page(response)
{
    // Grab the search tokens to output: 
        // Results for 'search_tokens'
    var search_tokens = query_string.substr(6).replace('+', ' ')
    $('#results_header').append("'" + search_tokens + "'")

    // Parse the JSON array from response, list out the urls as links
    for(let i = 0; i < response.length; i++)
        $('#url_table').append('<a href="' + response[i]['url'] + '"> ' + response[i]['url'] + '</a>' + '<br>');
}

$(document).ready(function(){
    // Send a request to api/results with our query
    // Should return a response in the form of a JSON array, as defined in app.py
        // Pass the JSON array from the response to populate_page(response)
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