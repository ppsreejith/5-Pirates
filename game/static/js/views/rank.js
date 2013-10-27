define(['jquery','lodash','backbone','models/rank'],function($,_,Backbone,RankList){

var RankView = Backbone.View.extend({
    el:'div.leaderBoard',
    initialize:function(){
	var that = this;
	this.rankCollection = new RankList();
	this.rankCollection.fetch({
	    success:function(){
		that.render();
	    }
	});
    },
    render:function(){
	var currentRanks = this.rankCollection.models();
	for(rank in currentRanks){
	    
	}
    }
});

});
