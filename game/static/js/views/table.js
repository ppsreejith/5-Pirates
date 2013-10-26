define(['jquery','lodash','backbone','models/round'],function($,_,Backbone, Round){

var TableView = Backbone.View.extend({
    el:'div.homeTable',
    userPosition:1,
    position:1,
    events:{
	"change input":"changed",
    },
    changed:function(e){
	var sum = 0, form = $(e.target.parentElement);
	form.find("input.valContent").each(function(i,e){
	    sum += parseInt(e.value);
	});
	if(e.target.value > 100 || sum > 100){
	    form.find("span.labelText.scrollError")[0].innerHTML= "You cant give away more than 100";
	    return;
	}
	form.find("span.yourMoneyScroll").html(100-sum);
	form.find("span.labelText.scrollError")[0].innerHTML= "";
    },
    template:_.template($("#tableTemplate").html()),
    initialize:function(){
	_.bindAll(this, "changed");
	var that = this;
	globalEvent.on("change:position",function(newP){
	    that.position = newP.position;
	    that.render();
	});
	globalEvent.on("scroll:submit",function(){
	    that.tableCollection.fetch({success:function(){
		that.render();
	    }});
	});
	this.tableCollection =new Round.Tables(),
	this.tableCollection.fetch({success:function(){
	    that.render();
	}});
    },
    render:function(){
	var currentTables = this.tableCollection.where({userPos:this.position})
	var html = "";
	var obj = {};
	var accepting = "<span class=\"labelText\">Minimum that you are willing to accept from:</span><br/>";
	var distributing = "<span class=\"labelText\">Proposed distribution when in command:</span><br/>";
	console.log(distributing);
	if(this.position == 1)
	    accepting = "";
	if(this.position == 5)
	    distributing = "";
	var i = 1;
	for(tabIn in currentTables){
	    table = currentTables[tabIn];
	    if(table.get('position') == table.get('userPos')){
		obj["yourCoins"] = table.get('amount');
		obj["pl5"] = table.get('userPos');
	    }
	    else{
		obj["p"+i] = table.get('amount');
		obj["pl"+(i++)] = table.get('position');
	    }
	    if(table.get('position') > table.get('userPos')){
		obj["v"+(i-1)] = "ent";
	    }
	    else{
		obj["v"+(i-1)] = "";
	    }
	    obj["s"+table.get('position')] = "";
	}
	obj["s1"] = accepting;
	obj["s"+table.get('userPos')] = distributing;
	this.$el.html(this.template(obj));
    }
});

return TableView;

});



