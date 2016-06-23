/* vote function */

$(document).ready(function() {

$('.vote a').each(function(){
	var s = window.localStorage;
	var aid = $(this).attr('href');
	if (s.getItem(aid) != null) {
		$(this).addClass('voted');
	}
});

$('.vote a').on('click', function(e) {
	e.preventDefault();
	var s = window.localStorage;
	var aid = $(this).attr('href');
	if (s.getItem(aid) != null) {
		return;
	}
	else {
		$(this).addClass("voted");
		$.post("/api/vote", {aid: aid}).done(function(r){
			if (r['err'] == 0) {
				s.setItem(aid, 1);
			}
			else {
				$(".vote a[href=" + aid + "]").removeClass("voted");
			}
		});
}});

});
