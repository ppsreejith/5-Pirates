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
require(['jquery','domReady','backbone','views/pirates','views/table'],function($,domReady,Backbone,Pirates,Tables){

    domReady(function(){
	//Event related stuff
	globalEvent = {}
	globalEvent = _.extend({}, Backbone.Events);
	
	$("div.homeMiniMap > div.miniMapBox").on("click",function(e){
	    var no = parseInt(e.target.innerHTML);
	    if (""+no == document.querySelector("div.miniMapBox5").innerHTML){
		return;
	    }
	    globalEvent.trigger("change:position",{position:no});
	    var arr = [1,2,3,4,5];
	    arr.splice(arr.indexOf(no),1);
	    arr.push(no);
	    $("div.homeMiniMap > div.miniMapBox").each(function(index,el){
		el.innerHTML = arr[index];
	    });
	});
	
	//scroll form submit
	window.exitScroll = function(){
	    $("div.homeTable form.scrollInput").toggleClass("rolled");
	}
	
	window.scrollSubmit = function(){
	    var form = $("div.homeTable form.scrollInput");
	    var formvals = form.find("input"),sum=0,fc=0;
	    console.log(formvals);
	    for(fc=0;fc++;fc<4){
		console.log(formvals[fc]);
		sum+=parseInt(formvals[fc].val());
		console.log(sum);
	    }
	    if (sum > 100){
		form.find("span.labelText.scrollError")[0].innerHTML= "You cant give away more than 100";
		return;
	    }
	    form.find("span.scrollSubmit").innerHTML="Please Wait";
	    $.ajax({type:"post",url:"/game/setalloc",data:form.serialize(),success:function(){
		globalEvent.trigger("scroll:submit");
	    },error:function(){
		form.find("span.scrollSubmit").innerHTML="Submit";
		form.find("span.labelText.scrollError").innerHTML="Please check your values";
	    }});
	}

	var Workspace = Backbone.Router.extend({

	    routes: {
		"play":                 "play",    // #help
		"rules":        "rules",  // #search/kiwis
		"dashboard": "dashboard"   // #search/kiwis/p7
	    },

	    play:function(){
		$("div.active").removeClass("active");
		$("div.mainOptionHome").addClass("active");
	    },
	    rules:function(){
		$("div.active").removeClass("active");
		$("div.mainOptionRules").addClass("active");
	    },
	    dashboard:function(){
		$("div.active").removeClass("active");
		$("div.mainOptionDashboard").addClass("active");
	    }

	});

	var route = new Workspace();
	Backbone.history.start();
	
	//Main menu
	$('div.menuDropDown > a,img.topMenu').click(function(){
	    $('div.menuDropDown').toggleClass('ascend');
	});
	
	//Initializing stuff
	var pirateView = new Pirates();
	var tableView = new Tables();
    });
    return {};
});
