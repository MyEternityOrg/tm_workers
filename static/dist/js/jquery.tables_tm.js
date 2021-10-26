(function ($) {
	$('.clickable-row').css('cursor', 'pointer');
	$(".clickable-row").click(function () {
		window.location = $(this).data("href");
	});
})(jQuery)