window.addEventListener("DOMContentLoaded", async function () {
  console.log("Page started successfully at " + new Date().toLocaleTimeString());
  let serverUrl;
  try {
    // Fetch configuration from the main process
    const config = await window.electron.invoke('getConfig');
     serverUrl = config.serverUrl; // Accessing the serverUrl from config
    console.log("Config loaded successfully:", config);
    console.log("Success 1");
  } catch (error) {
    console.error("Error occurred during config loading:", error);
  }

  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const message = document.getElementById("h2_message");
  const colorizeButton = document.getElementById("colorize-button");
  const imagePreview = document.getElementsByClassName("imagepreviewbox")[0];
  const sourceImage = document.getElementById("source-image");
  const imagewrapper = document.getElementsByClassName("image-wrapper")[0];
  const downloadButton = document.getElementById("download-button");
  let didColorize;
  let filename;

  let uploadedFile = null; // Global variable to store the file
  let colorizedImage = null; // Global variable to store the colorized image

  function showSwal(options) {
    Swal.fire({
      customClass: { container: "custom-swal" },
      ...options,
    });
  }
  console.log("success 2");

  if (dropZone) {
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
      const files = e.dataTransfer.files;
      handleFiles(files);
    });

    dropZone.addEventListener("click", () => {
      fileInput.click();
    });
  }

  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const files = fileInput.files;
      handleFiles(files);
    });
  }

  function handleFiles(files) {
    console.log("Files:", files);
    const file = files[0];
    if (file.type.startsWith("image/")) {
      showSwal({
        title: "Image dropped!",
        text: file.name,
        icon: "success",
      });
    } else {
      showSwal({
        title: "Invalid file type",
        text: "Please drop an image file",
        icon: "error",
      });
      return;
    }
    if (files.length > 1) {
      showSwal({
        title: "You can only upload one file at a time",
        icon: "error",
      });
      return;
    }
    console.log("Success 3");
    // Remove the upload zone
    document.getElementsByClassName("upload")[0].style.display = "none";
    // Display the image
    imagePreview.style.display = "block";
    imagePreview.getElementsByTagName("img")[0].src = URL.createObjectURL(file);
    message.innerText = "Press Colorize to colorize the image";

    // Enable colorize button
    colorizeButton.disabled = false;

    // Store file in the global variable
    uploadedFile = file;
  }

  function progressBar(ready = false) {
    showSwal({
      title: "Sit tight while the magic happens!",
      html: '<b></b><br/><br/><div id="progress-bar"><div></div></div>',
      allowOutsideClick: false,
      showConfirmButton: false,
      didOpen: () => {
        Swal.showLoading();
        const progressBar = document.querySelector("#progress-bar div");

        if (ready) {
          progressBar.style.width = `100%`;
          Swal.close();
          return;
        }

        let progress = 0;
        const interval = setInterval(() => {
          if (progress < 80) {
            progress += 8;
          }
          progressBar.style.width = `${progress}%`;
          if (progress >= 100) {
            clearInterval(interval);
            Swal.close();
          }
        }, 1000);
      },
    });
  }

  if (colorizeButton) {
    colorizeButton.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent default form submission

      const file = uploadedFile;

      if (!file) {
        showSwal({
          title: "No image selected",
          text: "Please upload an image first",
          icon: "error",
        });
        return;
      }

      console.log("File:", file);
      progressBar();

      // Set source image
      sourceImage.src = URL.createObjectURL(file);

      const renderFactor = localStorage.getItem("renderFactor");
      const model = localStorage.getItem("model");
      let artistic = false;
      const formData = new FormData();
      formData.append("image", file);
      if (model === "artistic") {
        artistic = true;
      }

      if (renderFactor === null || isNaN(renderFactor)) {
        formData.append("render_factor", 35);
      } else {
        formData.append("render_factor", renderFactor);
      }
      formData.append("artistic", artistic);

      // Use the server URL from config
      fetch(`${serverUrl}/colorize/image`, {
        method: "POST",
        body: formData,
      })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
          })
          .then((data) => {
            if (data.error) {
              showSwal({
                title: "Error",
                text: data.error,
                icon: "error",
              });
            } else {
              // Assuming the API returns a base64 encoded image
              colorizedImage = "data:image/png;base64," + data.image;
              document.getElementById("colorized-image").src = colorizedImage;
              console.log("The image was colorized successfully");

              // Hide the image preview and show the comparison images
              imagePreview.style.display = "none";
              // Apply fade-in effect to the colorized image
              imagewrapper.style.opacity = "0";
              imagewrapper.style.display = "flex";
              setTimeout(() => {
                imagewrapper.style.opacity = "1";
              }, 0);
              message.innerText = "Image colorized successfully!";
              didColorize = true;

              let history =
                  JSON.parse(localStorage.getItem("ProcessedHistory")) || [];

              const Processed = {
                file: uploadedFile.name,
                time: new Date().toLocaleTimeString(),
                date: new Date().toLocaleDateString(),
              };
              history.push(Processed);

              if (localStorage.getItem("history") === "true") {
                localStorage.setItem("ProcessedHistory", JSON.stringify(history));
              }

              downloadButton.disabled = false;
              progressBar(true);
            }
          })
          .catch((error) => {
            showSwal({
              title: "Error",
              text: "An error occurred while colorizing the image",
              icon: "error",
            });
            console.error("Error:", error);
          });
    });
  }

  if (downloadButton) {
    downloadButton.addEventListener("click", function () {
      if (colorizedImage) {
        const link = document.createElement("a");
        link.href = colorizedImage;
        link.download = "colorized_image.png";
        link.click();
      } else {
        showSwal({
          title: "No image to download",
          text: "Please colorize an image first",
          icon: "error",
        });
      }
    });
  }
});
