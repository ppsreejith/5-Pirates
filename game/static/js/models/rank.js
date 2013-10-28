define(['lodash','backbone'], function(_,Backbone){

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
    comparator:function(model) {
	return model.get('rank');
    },
});

return RankList;

});
