document.addEventListener("DOMContentLoaded", function () {
  console.log(
    "Page started successfully at " + new Date().toLocaleTimeString()
  );
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  let message = document.getElementById("h2_message");
  const colorizeButton = document.getElementById("colorize-button");
  const imagePreview = document.getElementsByClassName("imagepreviewbox")[0];
  const sourceImage = document.getElementById("source-image");
  const imagewrapper = document.getElementsByClassName("image-wrapper")[0];
  const downloadButton = document.getElementById("download-button");

  let uploadedFile = null; // Global variable to store the file
  let colorizedImage = null; // Global variable to store the colorized image

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

  fileInput.addEventListener("change", () => {
    const files = fileInput.files;
    handleFiles(files);
  });

  function handleFiles(files) {
    console.log("Files:", files);
    const file = files[0];
    if (file.type.startsWith("image/")) {
      swal.fire("Image dropped!", file.name, "success");
    } else {
      swal.fire("Invalid file type", "Please drop an image file", "error");
      return;
    }
    if (files.length > 1) {
      swal.fire("You can only upload one file at a time", "", "error");
      return;
    }

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

  colorizeButton.addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default form submission

    const file = uploadedFile;

    if (!file) {
      swal.fire("No image selected", "Please upload an image first", "error");
      return;
    }

    console.log("File:", file);

    // Set source image
    sourceImage.src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("image", file);
    formData.append("render_factor", 35); // or get this value from user input

    fetch("http://127.0.0.1:5000/colorize", {
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
          swal.fire("Error", data.error, "error");
        } else {
          // Assuming the API returns a base64 encoded image
          colorizedImage = "data:image/png;base64," + data.image;
          document.getElementById("colorized-image").src = colorizedImage;
          console.log("The image was colorized successfully");

          // Hide the image preview and show the comparison images
          imagePreview.style.display = "none";
          imagewrapper.style.display = "flex";
          message.innerText = "Image colorized successfully!";

          // Enable download button
          downloadButton.disabled = false;
        }
      })
      .catch((error) => {
        swal.fire(
          "Error",
          "An error occurred while colorizing the image",
          "error"
        );
        console.error("Error:", error);
      });
  });

  // Download button event listener
  downloadButton.addEventListener("click", function () {
    if (colorizedImage) {
      const link = document.createElement("a");
      link.href = colorizedImage;
      link.download = "colorized_image.png"; // Set the download filename
      link.click();
    } else {
      swal.fire(
        "No image to download",
        "Please colorize an image first",
        "error"
      );
    }
  });
});
