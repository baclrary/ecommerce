const stars = document.querySelectorAll('#star-rating svg');
let selectedRating = null;

for (let i = 0; i < stars.length; i++) {
    stars[i].addEventListener('mouseover', function () {
        // only change colors if no rating has been selected
        if (selectedRating === null) {
            for (let j = 0; j <= i; j++) {
                stars[j].classList.add('text-yellow-400');
                stars[j].classList.remove('text-gray-400');
            }
            for (let k = i + 1; k < stars.length; k++) {
                stars[k].classList.add('text-gray-400');
                stars[k].classList.remove('text-yellow-400');
            }
        }
    });

    stars[i].addEventListener('mouseout', function () {
        // only change colors if no rating has been selected
        if (selectedRating === null) {
            for (let j = 0; j < stars.length; j++) {
                stars[j].classList.add('text-gray-400');
                stars[j].classList.remove('text-yellow-400');
            }
        }
    });

    stars[i].addEventListener('click', function () {
        // set selected rating
        selectedRating = i + 1;

        // change colors based on selected rating
        for (let j = 0; j < selectedRating; j++) {
            stars[j].classList.add('text-yellow-400');
            stars[j].classList.remove('text-gray-400');
        }
        for (let k = selectedRating; k < stars.length; k++) {
            stars[k].classList.add('text-gray-400');
            stars[k].classList.remove('text-yellow-400');
        }

        // save selected rating to your backend server here
    });
}


