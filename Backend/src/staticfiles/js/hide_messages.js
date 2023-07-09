document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        const messages = document.querySelectorAll('[role="alert"]');
        messages.forEach(function (message) {
            message.style.display = 'none';
        });
    }, 5000);
});
