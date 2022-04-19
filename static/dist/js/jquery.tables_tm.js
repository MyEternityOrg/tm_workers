(function ($) {
    $('.clickable-row').css('cursor', 'pointer');
    $(".clickable-row").click(function () {
        window.location = $(this).data("href");
    });
})(jQuery);

(function ($) {
    $('.clickable-row_np').css('cursor', 'pointer');
    $(".clickable-row_np").click(function () {
        window.location = $(this).data("href");
        // window.open($(this).data("href"), "_blank");
    });
})(jQuery);