define(['jquery','lodash','backbone','models/round'],function($,_,Backbone, Round){

var TableView = Backbone.View.extend({
    el:'div.homeTable',
    userPosition:1,
    position:1,
    template:_.template($("#tableTemplate").html()),
    initialize:function(){
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
	var accepting = "<span class=\"labelText\">Accept from:</span><br/>"
	var distributing = "<span class=\"labelText\">Distributing to:</span><br/>"
	if(table.position == 1)
	    accepting = "";
	if(table.position == 5)
	    distributing = "";
	var i = 1;
	for(table in currentTables){
	    if(table.position == table.userPos){
		obj["yourCoins"] = table.amount;
		obj["pl5"] = table.userPos
	    }
	    else{
		obj["p"+table.position] = table.amount;
		obj["pl"+(i++)] = table.position;
	    }
	    obj["s"+table.position] = "";
	}
	obj["s1"] = accepting;
	obj["s"+table.userPos] = distributing;
	this.$el.html(this.template(obj));
    }
});

return TableView;

});



