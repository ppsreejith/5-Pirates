define(['backbone'],function(Backbone){

var Flag = Backbone.Model.extend({
    defaults: {
	src:"",
	userPos:0
    },
});

var Flags = Backbone.Collection.extend({
    model:Flag,
    url:'/game/flags'
});

var Table = Backbone.Model.extend({
    defaults:{
	position:0,
	userPos:0,
	amount:0,
    },
});

var Tables = Backbone.Collection.extend({
    model:Table,
    url:'/game/tables',
});

var Pirate = Backbone.Model.extend({
    defaults:{
	position:0,
	userPos:0,
	stars:0,
    },
});

var Pirates = Backbone.Collection.extend({
    model:Pirate,
    url:'/game/pirates',
});

var Round = Backbone.Model.extend({
    defaults:{
	userPos:0,
	amountArr:[0,0,0,0],
    },
});

var Rounds = Backbone.Collection.extend({
    model:Round,
});

return {
    Flags:Flags,
    Pirates:Pirates,
    Rounds:Rounds,
    Tables:Tables,
};

});
