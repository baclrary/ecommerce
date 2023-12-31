document.addEventListener('DOMContentLoaded', function() {
  let start = 0;
  const btnShowMore = document.getElementById('show-more-faq');

  function loadFaqs() {
    fetch('?start=' + start, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('faq-list').innerHTML += data.html;
      start += 5;
      if (!data.has_more) {
        // If there are no more FAQs, hide the "show more" button
        btnShowMore.style.display = 'none';
      }
    });
  }

  // Load the first 5 FAQs when the page loads
  loadFaqs();

  // Load more FAQs when the "show more" button is clicked
  btnShowMore.addEventListener('click', loadFaqs);
});


