let currentReplyBox = null; // New variable to store current active reply box

function handleReplyButtonClick(event) {
    // Check if a reply button was clicked
    if (!event.target.classList.contains('reply-btn')) return;

    let replyButton = event.target;

    // Use destructuring to fetch multiple attributes
    let {userId, userEmail, reviewId, replyReviewId, replyId, parentReplyId} = replyButton.dataset;

    // Check and form url
    let url = getURL(reviewId, replyReviewId, replyId, parentReplyId);

    // Close existing reply form if exists
    if (currentReplyBox) {
        currentReplyBox.remove();
        currentReplyBox = null;
    }

    let replyBox = createReplyBox(reviewId || replyReviewId, userEmail);
    replyButton.parentElement.insertAdjacentElement('afterend', replyBox);

    currentReplyBox = replyBox;

    document.querySelector(`#send-reply-${reviewId || replyReviewId}`).addEventListener('click', function () {
        handleSendReplyClick(reviewId || replyReviewId, replyId, userId, userEmail, url);
    });
}

function getURL(reviewId, replyReviewId, replyId, parentReplyId) {
    if (replyReviewId && replyId !== 'null') {
        return `/review/create-reply/${replyReviewId}/${replyId}/`;
    } else if (replyId && parentReplyId !== 'null') {
        return `/review/create-reply/${replyId}/${parentReplyId}/`;
    } else {
        return `/review/create-reply/${reviewId || replyReviewId}/`;
    }
}

function createReplyBox(id, userEmail) {
    var replyBox = document.createElement("div");
    replyBox.setAttribute("id", `reply-box-${id}`);
    replyBox.setAttribute("class", "mt-4 ml-4 rounded p-2");
    replyBox.innerHTML = `
            <div class="flex flex-col space-y-4 text-sm text-gray-500 mt-2 ml-4 bg-gray-50 pr-4 p-4">
                <div class="flex items-center space-x-4">
                    <div class="flex-none">
                        <img src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=256&h=256&q=80"
                             alt="" class="h-6 w-6 rounded-full bg-gray-100">
                    </div>
                    <div>
                        <h4 class="font-medium text-gray-700">${userEmail}</h4>
                    </div>
                </div>
                <div class="flex justify-between items-end">
                    <textarea id="reply-input-${id}" class="border-2 rounded px-3 py-2 w-full h-40 flex-1" placeholder="Write a reply..."></textarea>
                    <button class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" id="send-reply-${id}">Send</button>
                </div>
            </div>
            `;
    return replyBox;
}

function handleSendReplyClick(reviewIdOrReplyReviewId, replyId, userId, userEmail, url) {
    var replyText = document.querySelector(`#reply-input-${reviewIdOrReplyReviewId}`).value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'X-CSRFToken': getCookie('csrftoken') // You might need to include CSRF token in your request header
        },
        body: JSON.stringify({
            'review_id': reviewIdOrReplyReviewId, // this is the id of the review to which this reply belongs, regardless of its depth
            'parent_id': replyId, // this is the id of the parent reply, if this is a reply to a reply; otherwise, it's null
            'reply_text': replyText,
            'user_id': userId,
            'user_email': userEmail
        })
    })
        .then(response => response.json())
        .then(data => {
            displayNewReply(data, reviewIdOrReplyReviewId, userEmail, replyText);
            // remove the reply box after successfully sending the reply
            if (currentReplyBox) {
                currentReplyBox.remove();
                currentReplyBox = null;
            }
        })
        .catch((error) => console.error('Error:', error));
}

function displayNewReply(data, reviewIdOrReplyReviewId, userEmail, replyText) {
    // Assuming the data contains the new reply, you can display it

    var newReply = document.createElement("div");
    newReply.innerHTML = `
            <div class="flex space-x-4 text-sm text-gray-500 mt-2 ml-4 bg-gray-50 pr-4">
                <div class="flex-none py-2 border-l-2 border-gray-200">
                    <img src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=256&h=256&q=80"
                        alt="" class="ml-4 h-6 w-6 rounded-full bg-gray-100">
                </div>
                <div class="py-2">
                    <h4 class="font-medium text-gray-700">${userEmail}</h4>
                    <p>
                        <time datetime="2021-07-16">Now</time>
                    </p>
                    <p class="prose prose-sm mt-2 text-gray-700 whitespace-pre-line">${replyText}</p>
                    <div id="reactions" class="flex items-center mt-4">
                        <button class="like-btn" data-review="${data.reply.id}" data-model="reply">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                                 class="h-4 w-4 mr-1 text-gray-500 {% if user_reactions.replies|get_item:reply.id == 'like' %} text-emerald-600 {% endif %}">
                                <path d="M8 10V20M8 10L4 9.99998V20L8 20M8 10L13.1956 3.93847C13.6886 3.3633 14.4642 3.11604 15.1992 3.29977L15.2467 3.31166C16.5885 3.64711 17.1929 5.21057 16.4258 6.36135L14 9.99998H18.5604C19.8225 9.99998 20.7691 11.1546 20.5216 12.3922L19.3216 18.3922C19.1346 19.3271 18.3138 20 17.3604 20L8 20"
                                      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <span class="likes-${data.reply.id} mr-4 text-emerald-600">0</span>
                        <button class="dislike-btn" data-review="${data.reply.id}" data-model="reply">
                            <svg xmlns="http://www.w3.org/2000/svg" stroke="currentColor" fill="none"
                         xmlns:xlink="http://www.w3.org/1999/xlink"
                         viewBox="0 0 1000 1000"
                         class="h-3 w-3 mr-2 text-gray-500 hover:text-pink-600 {% if user_reactions.reviews|get_item:review.id == "dislike" %} text-pink-600 {% endif %}">
                        <g transform="matrix(-54.2417 0 0 -54.2417 500.0003 500.0002)" id="690888">
                            <path
                                    stroke-width="1" stroke-linecap="round" stroke-linejoin="round"
                                    vector-effect="non-scaling-stroke"
                                    transform=" translate(-12.2806, -11.62)"
                                    d="M 8 10 V 20 M 8 10 L 4 9.99998 V 20 L 8 20 M 8 10 L 13.1956 3.93847 C 13.6886 3.3633 14.4642 3.11604 15.1992 3.29977 L 15.2467 3.31166 C 16.5885 3.64711 17.1929 5.21057 16.4258 6.36135 L 14 9.99998 H 18.5604 C 19.8225 9.99998 20.7691 11.1546 20.5216 12.3922 L 19.3216 18.3922 C 19.1346 19.3271 18.3138 20 17.3604 20 L 8 20">
                            </path>
                        </g>
                    </svg>
                        </button>
                        <span class="dislikes-${data.reply.id} mr-2 text-pink-600">0</span>
                    </div>
<!--                    <span class="px-2 border-gray-300">|</span>-->
<!--                    <button class="reply-btn mr-3 text-indigo-600" data-user-id="{{ request.user.id }}" data-user-email="{{ request.user.email }}"  data-review-id="{{ review.id }}" data-parent-reply-id="null">Reply</button>-->
                </div>
            </div>
        `;
    document.querySelector(`#reply-box-${reviewIdOrReplyReviewId}`).insertAdjacentElement('afterend', newReply);
}

document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', handleReplyButtonClick);
});
