/* global $, _, crossfilter, d3  */

(function(nbviz) {
    'use strict';

    // var winners_args = {
    //   "projection":JSON.stringify( {"mini_bio":0, "bio_image":0} )
    // };
    var query_winners = 'winners?projection=' +
        JSON.stringify( {"mini_bio":0, "bio_image":0} );

    var q = queue()
        .defer(d3.json, "static/data/world-110m.json")
        .defer(d3.csv, "static/data/world-country-names-nobel.csv")
        // .defer(d3.json, "data/nobel_winners_cleaned.json")
        .defer(d3.json, "static/data/winning_country_data.json");
        // .defer(d3.json, "static/data/nobel_winners_biopic.json")
    if(window.$STATIC_API){
        q.defer(nbviz.getDataFromAPI, '_winners');
    }
    else{
        q.defer(nbviz.getDataFromAPI, query_winners);
    }

    q.await(ready);

    function ready(error, worldMap, countryNames, countryData, winnersData) {
        // LOG ANY ERROR TO CONSOLE
        if(error){
            return console.warn(error);
        }
        // STORE OUR COUNTRY-DATA DATASET
        nbviz.data.countryData = countryData;
        // MAKE OUR FILTER AND ITS DIMENSIONS
        nbviz.makeFilterAndDimensions(winnersData);
        // INITIALIZE MENU AND MAP
        nbviz.initMenu();
        nbviz.initMap(worldMap, countryNames);
        // TRIGGER UPDATE WITH FULL WINNERS' DATASET
        nbviz.onDataChange();
    }
}(window.nbviz = window.nbviz || {}));
