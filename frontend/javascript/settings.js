document.addEventListener("DOMContentLoaded", function () {
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabs = document.querySelectorAll(".settings-tab");
  const renderFactor = document.getElementById("render-factor");
  const model = document.getElementById("ai-model");
  const historyToggle = document.getElementById("history-switch");

  function showSwal(options) {
    Swal.fire({
      customClass: { container: "custom-swal" },
      ...options,
    });
  }
  const storedModel = localStorage.getItem("model");
  model.value = storedModel || "stable";
  localStorage.setItem("model", model.value);

  model.addEventListener("change", function () {
    localStorage.setItem("model", this.value);
    console.log("Model is set to ", localStorage.getItem("model"));
  });

  renderFactor.addEventListener("change", function () {
    const value = parseFloat(this.value);
    const currentValue = localStorage.getItem("renderFactor");

    if (isNaN(value)) {
      showSwal({
        title: "Error",
        text: "Render factor must be a number",
        icon: "error",
        allowOutsideClick: false,
      });
      if (currentValue != null) {
        renderFactor.value = currentValue;
      } else {
        renderFactor.value = 35;
      }
      return;
    }
    if (value < 10 || value > 40) {
      showSwal({
        title: "Error",
        text: "The render factor must be between 10 and 40",
        icon: "error",
        allowOutsideClick: false,
      });
      renderFactor.value = currentValue;
      return;
    }

    localStorage.setItem("renderFactor", value);
    console.log(
      "Render Factor is set to",
      localStorage.getItem("renderFactor")
    );
  });

  historyToggle.addEventListener("change", function () {
    localStorage.setItem("history", this.checked ? "true" : "false");
    console.log("History is set to", localStorage.getItem("history"));
  });
  historyToggle.checked = localStorage.getItem("history") === "true";

  const renderFactorValue = localStorage.getItem("renderFactor");
  renderFactor.value = renderFactorValue || 35;

  const modelValue = localStorage.getItem("model");
  if (modelValue) {
    model.value = modelValue;
  }
});
