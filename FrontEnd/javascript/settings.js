document.addEventListener("DOMContentLoaded", function () {
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabs = document.querySelectorAll(".settings-tab");
  const renderFactor = document.getElementById("render-factor");
  const model = document.getElementById("ai-model");

  // Wrapper function to show SweetAlert with global styles
  function showSwal(options) {
    Swal.fire({
      customClass: { container: "custom-swal" },
      ...options,
    });
  }
  // Retrieve and set the model value from localStorage
  const storedModel = localStorage.getItem("model");
  model.value = storedModel || "stable";
  localStorage.setItem("model", model.value);

  // Update localStorage when the model selection changes
  model.addEventListener("change", function () {
    localStorage.setItem("model", this.value);
    console.log("Model is set to ", localStorage.getItem("model"));
  });

  renderFactor.addEventListener("change", function () {
    const value = parseFloat(this.value);
    const currentValue = localStorage.getItem('renderFactor');

    if (isNaN(value)) {
      showSwal({
        title: "Error",
        text: "Render factor must be a number",
        icon: "error",
        allowOutsideClick: false
      });
      if (currentValue != null) {
        renderFactor.value = currentValue;
      } else {
        renderFactor.value = 35;
      }
      return;
    }
    if(value<35 || value>45){
      showSwal({
        title: "Error",
        text: "The render factor must be between 35 and 45",
        icon:"error",
        allowOutsideClick: false
      });
      renderFactor.value=currentValue;
      return;
    }

    localStorage.setItem('renderFactor', value);
    console.log("Render Factor is set to", localStorage.getItem('renderFactor'));
  });

  // tabLinks.forEach((link) => {
  //   link.addEventListener("click", function (e) {
  //     e.preventDefault();
  //     const targetTab = this.getAttribute("data-tab");
  //
  //     // Remove active class from all links and tabs
  //     tabLinks.forEach((link) => link.classList.remove("active"));
  //     tabs.forEach((tab) => tab.classList.remove("active"));
  //
  //     // Add active class to clicked link and show the related tab
  //     this.classList.add("active");
  //     document.getElementById(targetTab).classList.add("active");
  //   });
  // });
  //
  // // Set the default active tab if none is set
  // const defaultActiveTab = document.querySelector(".tab-link.active");
  // if (defaultActiveTab) {
  //   defaultActiveTab.click();
  // } else if (tabLinks.length > 0) {
  //   tabLinks[0].click();
  // }

  // Make the render factor value match
  const renderFactorValue = localStorage.getItem('renderFactor');
  renderFactor.value = renderFactorValue || 35;

  // Make the selected model match
  const modelValue = localStorage.getItem('model');
  if (modelValue) {
    model.value = modelValue;
  }
});