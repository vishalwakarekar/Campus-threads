// script.js
let index = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function changeSlide(n) {
    slides[index].classList.remove('active');
    dots[index].classList.remove('active');
    index = (index + n + slides.length) % slides.length;
    slides[index].classList.add('active');
    dots[index].classList.add('active');
}

function currentSlide(n) {
    slides[index].classList.remove('active');
    dots[index].classList.remove('active');
    index = n;
    slides[index].classList.add('active');
    dots[index].classList.add('active');
}

function autoSlide() {
    changeSlide(1);
    setTimeout(autoSlide, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(autoSlide, 3000);
});