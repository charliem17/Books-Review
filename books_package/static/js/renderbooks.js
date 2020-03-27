// Used by search_page in search.html

const body = document.documentElement;
const books = document.querySelectorAll('.books-container .book');

const renderIncrement = 6;
let initialRender = 8;
const loadOffset = 200; // Pixels from bottom to render more books

const initialSetup = () => {

    if(initialRender > books.length) {
        initialRender = books.length;
    }

    for(let i = 0; i < initialRender; i++) {
        books[i].style.display = "initial";
    }
}

initialSetup();

window.addEventListener('scroll', () => {

    if(window.scrollY + window.innerHeight >= body.scrollHeight - loadOffset) {
        if(initialRender + renderIncrement <= books.length) {
            loadMore(initialRender, initialRender + renderIncrement);
        } else {
            loadMore(initialRender, books.length)
        }
    }
});

const loadMore = (start, end) => {
    for(let i = start; i < end; i++) {
        books[i].style.display = "initial";
    }
    initialRender = end;
}
