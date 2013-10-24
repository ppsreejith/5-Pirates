requirejs.config({
    baseUrl: "/static/js/",
    paths: { 
        'jquery': ['http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min','libs/jquery-min.js'],
        'lodash': 'libs/lodash.min',
	'domReady':'libs/domReady.min',
        'backbone': 'libs/backbone.min',
	'jsfxlib' : 'libs/jsfxlib.min',
    },
    shim: {
        'backbone': {
	    deps:['lodash','jquery'], 
	    exports: 'Backbone'
	},
	'lodash': {
	    exports: '_'
	}
    }
});

require([
    'jquery', 'lodash','backbone'
],
function($, _, Backbone){
    return {};
});

//Event Loaders, Dom Interaction
require(['jquery','domReady'],function($,domReady){
    domReady(function(){
	$('div.menuDropDown > a,img.topMenu').click(function(){
	    $('div.menuDropDown').toggleClass('ascend');
	});
    });
    return {};
});
