// document.addEventListener('DOMContentLoaded', function() {
//   let start = 0;
//   const btnShowMore = document.getElementById('show-more-reviews');
//
//   function loadFaqs() {
//     fetch('?start=' + start, {
//       headers: {
//         'X-Requested-With': 'XMLHttpRequest'
//       }
//     })
//     .then(response => response.json())
//     .then(data => {
//       document.getElementById('reviews-list').innerHTML += data.html;
//       start += 5;
//       if (!data.has_more) {
//         // If there are no more FAQs, hide the "show more" button
//         btnShowMore.style.display = 'none';
//       }
//     });
//   }
//
//   // Load the first 5 FAQs when the page loads
//   loadFaqs();
//
//   // Load more FAQs when the "show more" button is clicked
//   btnShowMore.addEventListener('click', loadFaqs);
// });
//
// //
//
// document.addEventListener('DOMContentLoaded', function() {
//   let startFaq = 0;
//   let startReview = 0;
//   const btnShowMoreFaq = document.getElementById('show-more-faq');
//   const btnShowMoreReviews = document.getElementById('show-more-reviews');
//
//   function loadFaqs() {
//     fetch('?start=' + startFaq + '&type=faq', {
//       headers: {
//         'X-Requested-With': 'XMLHttpRequest'
//       }
//     })
//     .then(response => response.json())
//     .then(data => {
//       document.getElementById('faq-list').innerHTML += data.html;
//       startFaq += 5;
//       if (!data.has_more) {
//         // If there are no more FAQs, hide the "show more" button
//         btnShowMoreFaq.style.display = 'none';
//       }
//     });
//   }
//
// //   function loadReviews() {
// //     fetch('?start=' + startReview + '&type=review', {
// //       headers: {
// //         'X-Requested-With': 'XMLHttpRequest'
// //       }
// //     })
// //     .then(response => response.json())
// //     .then(data => {
//       document.getElementById('reviews-list').innerHTML += data.html;
//       startReview += 5;
//       if (!data.has_more) {
//         // If there are no more reviews, hide the "show more" button
//         btnShowMoreReviews.style.display = 'none';
//       }
//     });
//   }
//
//   // Load the first 5 FAQs and reviews when the page loads
//   loadFaqs();
//   loadReviews();
//
//   // Load more FAQs when the "show more" button is clicked
//   btnShowMoreFaq.addEventListener('click', loadFaqs);
//
//   // Load more reviews when the "show more" button is clicked
//   btnShowMoreReviews.addEventListener('click', loadReviews);
// });
