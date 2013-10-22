define(['lodash', 'backbone'], function(_,Backbone){

var Rank = Backbone.Model.extend({
    initialize: function(rank, username, score){
       this.rank = rank;
       this.username = username;
       this.score = score;
    },

    validate:function(){
	
    },
});

var RankList = Backbone.Collection.extend({
    model:Rank,
    url:'/game/leaderboard',
})

});
