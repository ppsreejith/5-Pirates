requirejs.config({
    baseUrl: "/static/js/",
    paths: { 
        'jquery': ['http//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min','libs/jquery-min.js'],
        'lodash': 'libs/lodash.min',
        'backbone': 'libs/backbone.min',
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
