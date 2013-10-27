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
	    var dashMess={
		"1":"Ship 1: Queen Anne's Revenge. You are First in command (Player 1).<br/><br/>The characters that you see here are your opponents on this ship. The mini map on the bottom left of the screen gives your current ship and position in hierarchy. The stars above each player's head tell his skill level from 1 star to 3 stars. Click on the scroll kept on the table to make your moves as player 1. Then, click on the ship number on the mini map to move to another ship. For today’s sessions you can edit your submissions multiple times. In future, this may be possible only with a penalty.",
		"2":"Ship 2: Carolina. You are Second in command (Player 2).<br/><br/>The characters that you see here are your opponents on this ship. The mini map on the bottom left of the screen gives your current ship and position in hierarchy. The stars above each player's head tell his skill level from 1 star to 3 stars.<br/>click on the scroll kept on the table to make your moves as player 2. Then, click on the ship number on the mini map to move to another ship. For today’s sessions you can edit your submissions multiple times. In future, this may be possible only with a penalty.",
		"3":"Whydah Galley. You are Third in command (Player 3).<br/><br/>The characters that you see here are your opponents on this ship. The mini map on the bottom left of the screen gives your current ship and position in hierarchy. The stars above each player's head tell his skill level from 1 star to 3 stars.<br/>click on the scroll kept on the table to make your moves as player 3. Then, click on the ship number on the mini map to move to another ship. For today’s sessions you can edit your submissions multiple times. In future, this may be possible only with a penalty.",
		"4":"Adventure Galley. You are Fourth in command (Player 4).<br/><br/>The characters that you see here are your opponents on this ship. The mini map on the bottom left of the screen gives your current ship and position in hierarchy. The stars above each player's head tell his skill level from 1 star to 3 stars.<br/>click on the scroll kept on the table to make your moves as player 4. Then, click on the ship number on the mini map to move to another ship. For today’s sessions you can edit your submissions multiple times. In future, this may be possible only with a penalty.",
		"5":"Royal Revenge. You are Last in command (Player 5).<br/><br/>The characters that you see here are your opponents on this ship. The mini map on the bottom left of the screen gives your current ship and position in hierarchy. The stars above each player's head tell his skill level from 1 star to 3 stars.<br/>click on the scroll kept on the table to make your moves as player 5. Then, click on the ship number on the mini map to move to another ship. For today’s sessions you can edit your submissions multiple times. In future, this may be possible only with a penalty."
	    };
	    var values = {
		"1":"first",
		"2":"second",
		"3":"third",
		"4":"fourth",
		"5":"fifth",
	    };
	    globalEvent.trigger("change:position",{position:no});
	    var arr = [1,2,3,4,5];
	    arr.splice(arr.indexOf(no),1);
	    arr.push(no);
	    var home = $("div.homeMiniMap"),last = 0;
	    home.find("div.miniMapBox").each(function(index,el){
		el.innerHTML = arr[index];
		last = arr[index];
	    });
	    home.find("span.MiniMapPosition").html(values[last]);
	    $("div.shipData").html(dashMess[last]);
	});
	
	//scroll form submit
	window.exitScroll = function(){
	    $("div.homeTable form.scrollInput").toggleClass("rolled");
	}
	
	window.scrollSubmit = function(){
	    var form = $("div.homeTable form.scrollInput");
	    var formvals = form.find("input.valContent"),sum=0,fc=0;
	    formvals.each(function(i,e){
		console.log(e);
		sum+=parseInt(e.value);
	    });
	    if (sum > 100){
		form.find("span.labelText.scrollError")[0].innerHTML= "You cant give away more than 100";
		return;
	    }
	    form.find("span.scrollSubmit")[0].innerHTML="Please Wait";
	    $.ajax({type:"post",url:"/game/setalloc",data:form.serialize(),success:function(data){
		submittedAll = parseInt(data);
		globalEvent.trigger("scroll:submit");
	    },error:function(){
		form.find("span.scrollSubmit").innerHTML="Submit";
		form.find("span.labelText.scrollError").innerHTML="Please check your values";
	    }});
	};
	var submittedAll = 0;

	var Workspace = Backbone.Router.extend({

	    routes: {
		"" : "dashboard",
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
	window.onbeforeunload = function (e) {
	    var arr = tableView.notSubmittedArray;
	    if(arr.length == 0){
		return False;
	    }
	    var message = "Avast!! You haven’t played in positions: "+arr.toString();
	    e = e || window.event;
	    // For IE and Firefox
	    if (e) {
		e.returnValue = message;
	    }

	    // For Safari
	    return message;
	};
    });
    return {};
});
