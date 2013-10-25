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
	if(this.position == 1)
	    accepting = "";
	if(this.position == 5)
	    distributing = "";
	var i = 1;
	for(tabIn in currentTables){
	    table = currentTables[tabIn];
	    console.log(table.get('position'));
	    if(table.get('position') == table.get('userPos')){
		obj["yourCoins"] = table.get('amount');
		obj["pl5"] = table.get('userPos');
	    }
	    else{
		obj["p"+i] = table.get('amount');
		obj["pl"+(i++)] = table.get('position');
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



