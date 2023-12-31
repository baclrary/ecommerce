document.addEventListener('DOMContentLoaded', function () {
    let startFaq = 0;
    let startReview = 0;
    const btnShowMoreFaq = document.getElementById('show-more-faq');
    const btnShowMoreReviews = document.getElementById('show-more-reviews');

    const pNoMoreReviews = document.getElementById('no-more-reviews');
    const pNoMoreFaq = document.getElementById('no-more-faq');

    const faqList = document.getElementById('faq-list');
    const reviewsList = document.getElementById('reviews-list');

    let observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === "childList") {
                $('.image-link').magnificPopup({
                    type: 'image',
                    gallery: {
                        enabled: true
                    }
                });

                $('.video-link').magnificPopup({
                    type: 'inline',
                    callbacks: {
                        open: function () {
                            // Play the video when lightbox opens
                            let video = $(this.content).find('video')[0];
                            if (video) {
                                video.play();
                            }
                        },
                        close: function () {
                            // Pause the video when lightbox closes
                            let video = $(this.content).find('video')[0];
                            if (video) {
                                video.pause();
                            }
                        }
                    }
                });
            }
        });
    });

    // Begin observing the review list for changes
    let config = {childList: true, subtree: true};
    observer.observe(document.getElementById('reviews-list'), config);


    function loadFaqs() {
        fetch('?start=' + startFaq + '&type=faq', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                faqList.innerHTML += data.html;
                startFaq += 5;
                if (!data.has_more) {
                    // If there are no more FAQs, hide the "show more" button
                    if (btnShowMoreFaq) {
                        btnShowMoreFaq.style.display = 'none';
                    }
                    if (pNoMoreFaq) {
                        pNoMoreFaq.style.display = 'block';
                    }
                }
            });
    }


    function loadReviews() {
        const reviewsContainer = document.getElementById('reviews-container');
        const previousScrollPosition = reviewsContainer.scrollTop; // Record the current scroll position

        fetch('?start=' + startReview + '&type=review', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                reviewsList.innerHTML += data.html;
                startReview += 5;
                reviewsContainer.scrollTo(0, previousScrollPosition);


                if (!data.has_more) {
                    // If there are no more reviews, hide the "show more" button
                    if (btnShowMoreReviews) {
                        btnShowMoreReviews.style.display = 'none';
                    }
                    if (pNoMoreReviews) {
                        pNoMoreReviews.style.display = 'block';
                    }
                }

            });
    }

    // Load the first 5 FAQs and reviews when the page loads

    if (faqList) {
        loadFaqs();

    }

    if (reviewsList) {
        loadReviews();
    }

    // Load more FAQs when the "show more" button is clicked
    if (btnShowMoreFaq) {
        btnShowMoreFaq.addEventListener('click', loadFaqs);
    }

    // Load more reviews when the "show more" button is clicked
    if (btnShowMoreReviews) {
        btnShowMoreReviews.addEventListener('click', loadReviews);
    }


    document.querySelectorAll('.like-svg').forEach(svg => {
        svg.addEventListener('click', function () {
            const reviewId = svg.dataset.reviewId; // Assuming reviewId is set as a data attribute on the SVG
            fetch(`/review/${reviewId}/like/`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector(`#likes-${reviewId}`).innerText = data.likes;
                });
        });
    });

    document.querySelectorAll('.dislike-svg').forEach(svg => {
        svg.addEventListener('click', function () {
            const reviewId = svg.dataset.reviewId;
            fetch(`/review/${reviewId}/dislike/`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector(`#dislikes-${reviewId}`).innerText = data.dislikes;
                });
        });
    });
});
