requirejs.config({
    baseUrl: statics+"js/",
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
require(['jquery','domReady','backbone','views/pirates','views/table','views/rank'],function($,domReady,Backbone,Pirates,Tables,RankView){

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
		"1":ship1,
		"2":ship2,
		"3":ship3,
		"4":ship4,
		"5":ship5,
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
		sum+=parseInt(e.value);
	    });
	    if (sum > 100){
		form.find("span.labelText.scrollError")[0].innerHTML= "You cant give away more than 100";
		return;
	    }
	    var formAccepts = form.find("input.valCont"), acceptFlag = false;
	    formAccepts.each(function(i,e){
		if (e.value > 100)
		    acceptFlag = true;
	    });
	    if (acceptFlag){
		form.find("span.labelText.scrollError")[0].innerHTML= "You cant ask for more 100";
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
	
	//History
	function createMessage(message,no){
	    if (message == null || message.length == 0)
		$("div.historyInfo > div.info").html("<h2>Sorry, This history is not available at the moment.</h2>");
	    else{
		window.message = message;
		var table = $("<table style='text-align:center;color:white;width:100%;margin-top:20px;'></table>");
		var row = $("<tr></tr>");
		var col = $("<th>Session</th>");
		row.append(col);
		for(i=1;i<=5;i++){
		    col = $("<th>Player "+i+"</th>");
		    row.append(col);
		}
		table.append(row);
		for(i=0;i<message.length;i++){
		    row = $("<tr></tr>");
		    row.append($("<td> "+message[i].session+"</td>"));
		    for(j=1;j<=5;j++){
			if (j<=no)
			    col = $("<td style='color:green;'>"+message[i][""+j]+"</td>");
			else
			    col = $("<td style='color:red;'>"+message[i][""+j]+"</td>");
			row.append(col);
		    }
		    table.append(row);
		}
	    }
	    $("div.historyInfo > div.info").html(table);
	    $("div.historyInfo").addClass("active");
	}
	
	window.removeMessage = function(){
	    $("div.historyInfo").removeClass("active");
	}
	
	$("div.pirates").on("click","img.pirate",function(){
	    createMessage($(this).data("history"),parseInt($(this.parentElement).attr("class")[6]));
	});
	
	//Main menu
	$('div.menuDropDown > a,img.topMenu').click(function(){
	    $('div.menuDropDown').toggleClass('ascend');
	});
	
	//Initializing stuff
	var pirateView = new Pirates();
	var tableView = new Tables();
	var ranks = new RankView();
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
