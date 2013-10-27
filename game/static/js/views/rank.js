define(['jquery','lodash','backbone','models/rank'],function($,_,Backbone,RankList){

var RankView = Backbone.View.extend({
    el:'div.leaderboardRanks',
    template:_.template($("#leaderBoardTemplate").html()),
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
	var currentRanks = this.rankCollection.models;
	html = "";
	for(rInd in currentRanks){
	    rank = currentRanks[rInd];
	    html += this.template(
		{'rank':rank.get('rank'),
		 'name':rank.get('username'),
		 'score':rank.get('score')}
				 );
	};
	this.$el.html(html);
    }
});

return RankView;

});
