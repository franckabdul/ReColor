//Function to handle the slideshow
const slides = document.querySelectorAll(".carousel-item");
const totalSlides = slides.length;
function showRandomSlide() {
  const randomIndex = Math.floor(Math.random() * totalSlides);
  const offset = -randomIndex * 100;

  const carousel = document.querySelector(".carousel");
  carousel.style.transition = "none";
  carousel.style.transform = `translateX(${offset}%)`;

  setTimeout(() => {
    carousel.style.transition = "transform 0.5s ease";
  }, 100);
}
function addCopyrightNote() {
  // Select all carousel items
  const items = document.querySelectorAll(".carousel-item");

  items.forEach((item) => {
    // Create the copyright note element
    const copyrightNote = document.createElement("div");
    copyrightNote.className = "copyright-note";
    copyrightNote.innerHTML = `© <i class="fa-brands fa-reddit"></i> r/TheWayWeWere`;

    // Append the copyright note to the carousel item
    item.appendChild(copyrightNote);
    console.log("Added a copyright note");
  });
}

function getStarted() {
  window.open("HTML/new.html", "_self");
}

document.addEventListener("DOMContentLoaded", () => {
  showRandomSlide();
  addCopyrightNote();
});
