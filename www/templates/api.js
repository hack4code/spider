
$(document).ready(function() {
	$.getJSON("/api/day", {day: "2016-06-24"}).done(function(data) {
		var entries = data["entries"];
		var categories = [];
		$.each(entries, function(key, val) {
			categories.push(key);
		});
		console.log(categories);
	});


});
