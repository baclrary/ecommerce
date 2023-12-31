$(document).ready(function () {
    var processing = false;  // Flag to check if a request is being processed

    $(document).on('click', '.like-btn', function (event) {

        if (processing) {
            return;  // If a request is being processed, we return and don't execute this click
        }
        processing = true;

        event.preventDefault();

        let object_id = $(this).data('review');
        let model_name = $(this).data('model');

        $.ajax({
            url: `/review/${object_id}/like/`,
            type: 'POST',
            data: {
                'id': object_id,
                'model_name': model_name,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (response) {
                processing = false;
                let likesElement = $(`.likes-${object_id}`);
                let dislikesElement = $(`.dislikes-${object_id}`);
                let currentLikes = parseInt(likesElement.text());
                let currentDislikes = parseInt(dislikesElement.text());

                let likeSVG = $(`.like-btn[data-review="${object_id}"] svg`);
                let dislikeSVG = $(`.dislike-btn[data-review="${object_id}"] svg`);

                if (response.status === 'added') {
                    likesElement.text(currentLikes + 1);
                    likeSVG.removeClass('text-gray-500');
                    likeSVG.addClass('text-emerald-600');
                    dislikeSVG.removeClass('text-pink-600');
                    dislikeSVG.addClass('text-gray-500');
                } else if (response.status === 'like_removed') {
                    likesElement.text(currentLikes - 1);
                    likeSVG.removeClass('text-emerald-600');
                    likeSVG.addClass('text-gray-500');
                } else if (response.status === 'switched_to_like') {
                    dislikesElement.text(currentDislikes - 1);
                    likesElement.text(currentLikes + 1);
                    likeSVG.removeClass('text-gray-500');
                    likeSVG.addClass('text-emerald-600');
                    dislikeSVG.removeClass('text-pink-600');
                    dislikeSVG.addClass('text-gray-500');
                }
            }
        });
    });

    $(document).on('click', '.dislike-btn', function (event) {
        if (processing) {
            return;  // If a request is being processed, we return and don't execute this click
        }
        processing = true;  // Set processing to true as we start a new request

        event.preventDefault();

        let object_id = $(this).data('review');
        let model_name = $(this).data('model');

        $.ajax({
            url: `/review/${object_id}/dislike/`,
            type: 'POST',
            data: {
                'id': object_id,
                'model_name': model_name,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (response) {
                processing = false;
                let likesElement = $(`.likes-${object_id}`);
                let dislikesElement = $(`.dislikes-${object_id}`);
                let currentLikes = parseInt(likesElement.text());
                let currentDislikes = parseInt(dislikesElement.text());

                let likeSVG = $(`.like-btn[data-review="${object_id}"] svg`);
                let dislikeSVG = $(`.dislike-btn[data-review="${object_id}"] svg`);

                if (response.status === 'added') {
                    dislikesElement.text(currentDislikes + 1);
                    dislikeSVG.removeClass('text-gray-500');
                    dislikeSVG.addClass('text-pink-600');
                    likeSVG.removeClass('text-emerald-600');
                    likeSVG.addClass('text-gray-500');
                } else if (response.status === 'dislike_removed') {
                    dislikesElement.text(currentDislikes - 1);
                    dislikeSVG.removeClass('text-pink-600');
                    dislikeSVG.addClass('text-gray-500');
                } else if (response.status === 'switched_to_dislike') {
                    likesElement.text(currentLikes - 1);
                    dislikesElement.text(currentDislikes + 1);
                    dislikeSVG.removeClass('text-gray-500');
                    dislikeSVG.addClass('text-pink-600');
                    likeSVG.removeClass('text-emerald-600');
                    likeSVG.addClass('text-gray-500');
                }
            }
        });
    });
});
