(function ($) {
    "use strict";

    $('.login-form').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() !== "") {
                $(this).addClass('login-focused');
            } else {
                $(this).removeClass('login-focused');
            }
        })
    })


})(jQuery);