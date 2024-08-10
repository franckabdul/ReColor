// Tab Switching Logic
document.addEventListener("DOMContentLoaded", function () {
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabs = document.querySelectorAll(".settings-tab");

  tabLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetTab = this.getAttribute("data-tab");

      // Remove active class from all links and tabs
      tabLinks.forEach((link) => link.classList.remove("active"));
      tabs.forEach((tab) => (tab.style.display = "none"));

      // Add active class to clicked link and show the related tab
      this.classList.add("active");
      document.getElementById(targetTab).style.display = "block";
    });
  });
});
