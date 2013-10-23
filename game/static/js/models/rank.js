define(['backbone'], function(Backbone){

var Rank = Backbone.Model.extend({
    defaults: {
	"rank":0,
	"username":"",
	"score":0
    },
});

var RankList = Backbone.Collection.extend({
    model:Rank,
    url:'/game/leaderboard',
});

return RankList;

});
