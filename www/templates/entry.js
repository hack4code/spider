$(document).ready(function() {
$('.category .link a').on('click', function(e){
	e.preventDefault();
	var cid = '#'+$(this).attr('href');
	$(cid).show().siblings().hide();
	$(this).parent('li').addClass('active').siblings().removeClass('active');
});

$('#clink1 a').trigger('click');

$('.spider a').on('click', function(e) {
	e.preventDefault();
	var url = "/p/" + $(this).attr("href");
	window.open(url);
});

$('.domain a').on('click', function(e) {
	e.preventDefault();
	var url = "http://" + $(this).text();
	window.open(url);
});

});

