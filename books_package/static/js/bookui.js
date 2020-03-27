// Used by book_page in book.html

openReviewUIBtn = document.querySelector('#open-review-ui');
submitBtn = document.querySelector('#review-submit');
cancelBtn = document.querySelector('#review-cancel');
reviewUI = document.querySelector('.review-ui');

openReviewUIBtn.addEventListener('click', () => {
    // Open review UI
    reviewUI.classList.add('show');
    submitBtn.style.pointerEvents = "initial";
});

submitBtn.addEventListener('click', () => {
    // Disables the chance for multiple submissions
    submitBtn.style.pointerEvents = "none";
});

cancelBtn.addEventListener('click', () => {
    // Close the UI
    reviewUI.classList.remove('show');
});

