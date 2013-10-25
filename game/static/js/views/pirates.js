define(['jquery','lodash','backbone','models/round'],function($,_,Backbone, Round){

var starData = {
1:"data:image/png;base64,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",
2:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAoCAYAAAA16j4lAAAGTElEQVR4Xu2baUxUVxTH/6JAWFzAlbSpC2gVbV1Qo7i1FYzUoLZGUj+4ti6RtHE3JNZEE5Nq3BIrJiYqsWq0bkTEitWkLlWrEbFxBTX1g1JcWARGRMT+7ygVYWa4F2bmnQ++5DGPeefe9z/nN+++e8+9rxEEb82aIUfJe/oUnSXKlK5PxayRxMC90TSkd2+kqePLlxHPj9PCtErXZw+XWMCtWuHS7t3o8+oVMGECLj1+jL6SAEvXVxUrqYAH9eyJ9KwsNFdCe/XC0ytXEMfDs0IgS9f3f5hEAubdcWHnTvQbMeK1zowMYPJkXMzLQ38JgKXrqx4jiYAHdO+OjKtX0ay6UH5XfP06YvjdBYshS9f3TnjEAW7bFn+lpKD/yJHvYjxyBJg6FecfPsRAKwFL11czNtIA9+vWDSd4pzZ1BLFrVxTfuoXPee6SRZCl66sVFlGAeXec27IFA0aNcozv0CFg1iz8mZuLwVYAlq7PUUwkAY6KiMDxnBy0cAWvQwfk37uH4bTJ8jJk6fochkMM4KAgHNu1C7GjR7vGdvAgMGUKMpjdqvGU9ixu6fqceW8l4BCK6sJdpSGjIyPx1bVraKeDic/pvJs3sZe257mrdKbaC3TKGthI16fliicAqzqZf7JvaqijANr35s3Ry8cHXW02tOf/PuHheMHhT+MePRC0cCEQEKClGaWlwOrVAIdSpeyQVd65gyYsWRkYiHuVlbhRVGRvvqvAq8/iajVL16cXBE0rTwAOaNoUWQx02IsX8OvYEeV8tlb06YOQzsRctbdsqalQ0+zJExIlyuzs15/MghXevo0mhO/r54dy/rD+LS5GJKvzFa6vQtNlLTNPAG4cHIzcAwfQOjZWS4PHjY4eBRISkEfAYarlEK6vqvVzS1w8AdgurE0b/JOaivYDLU1LAGfOAOPG4S4TJOHVIyZdn1voshKPAVYCOW7M2bMHEcOGuUuuWT0nTgCTJiH7wQN87KikdH1m3jq29ihgdUkm5rO2b0dEXByC3CFYt460NJROm4ZbnGaMclVGuj5df53ZeRywunBICM5u3YpPx471DuR9+2CbMQOZBQUYohMg6fp0fLAUsLo4e81/JCejHzs7gQ0RXFfZHTtgmzMH59mrVtku7U26Pm1Hahh65Q6uuiaD+PuaNYjm3K5HIDOPbUtKwulHj+qX5ZKurz6QvQpYCWzXDkeWLcNnbEI10xp6brF1eLZ8OY5zUUAdyU7X9UnXpxeNt1ZeB6wuHRaGVM4MDe/bF8Gmgh3ZnzuHkvHjcez+fYxzR33S9Zn4aAlgCmzFjs3d/HzH874mDrzpxJUWFuJDHhealnViL12ftptWAf6Cd+/+ixddTw3qehEVhaLMTHvTfEq3TB120vVpu2kV4B9mz8aqjRvhr63UheHMmXi+eTPm0STZHfWxDun6tN20BDBnfVLWr8fk6dO1dbo03LQJWLAAWzhL9Z07apSuz8RHSwDz+Xs1PR3d3ZWnPs13HsaMwd9MbPQ0cd6ZrXR9Jj5aAtjXF2VMRPhz2s4tG8Gq4ZetvNw9mTLp+kyCZgXgj5j/vc5kRJ25aTUTpLbBGkvsQkNhI2i1sOCBSQAc2ErXZ+SeFYC/HDQIvxBeqDOlnKxHYiLyb9zAfWXDJTofMJERytdZnG7R0SjgePgbGhwzikBtY+n6jNyzAvCiRYuwcuXK2jq5+gLz5sF26hTyOK5NpMVvb6ziWrRA8tChaLNuHQI7dapddv58YO1a8C/WGkWgtrF0fUbueR0w12Xt37ABX0+c+FYn04uYOxclhw/DxlUX3/PMr068SOBz++f4eASwFx7cuvVbq23b7D3pvUyeJBhFoIaxdH2mvnkdMAFlnzyJznz3FxzWYPFilHMqsYzHcyl+q6YD3/r7Yx2HWX6rVsFfLdZj0gQxMbjJ5bTdNOtwaCZdn6lvXgfMxW8vy8rgs2QJnrNJ9WFAl7Jz9JOpcGXP2Z8krqBczjv35dKl8Ocb9xUVFfCtT11VZaTrM/XN24C7sAnMJJRAPlNX8Dn7o6lgR/b8kawoKUESExTPuKT2E9rcrWe90vUZu+VtwGqdtOo8qS5WpbFa1wUa8zRXV2Mj9+rroE0uI12fiS92W28DNhb4vkDDIvAecMPiJ770e8DiETVM4H+TLfhHna46bAAAAABJRU5ErkJggg==",
3:"data:image/png;base64,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"
};

var PirateView = Backbone.View.extend({
    el:'div.pirates',
    position:1,
    template:_.template($("#pirateTemplate").html()),
    initialize:function(){
	var that = this;
	globalEvent.on("change:position",function(newP){
	    that.position = newP.position;
	    that.render();
	});
	this.pirateCollection = new Round.Pirates(),
	this.pirateCollection.fetch({success:function(){
	    that.render();
	}});
    },
    render:function(){
	var currentPirates = this.pirateCollection.where({userPos:this.position});
	var html = "";
	for(pirate in currentPirates){
	    html += this.template({position:pirate.position,
				   userPos:pirate.userPos,
				   stars:this.starData(pirate.stars)});
	}
	$el.html(html);
    }
});

return PirateView;

});
