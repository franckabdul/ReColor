//This will contain the javascript code that is common to all the pages of the website

document.addEventListener("DOMContentLoaded", () => {

    function setColorVariable(variableName, value) {
        document.documentElement.style.setProperty(variableName, value);
    }

    function dark_light_mode() {
        const darkMode = localStorage.getItem('darkMode');
        // const logo=document.getElementById("logo");

        if (darkMode === 'true') {
            setColorVariable('--primary-color', "#468189");
            setColorVariable('--secondary-color', "#d49a6a");
            setColorVariable('--tertiary-color', "#faebd7");
            setColorVariable('--bcgrd', "#333131");
            // logo.src = "../images/ReColordark.png";
        } else {
            setColorVariable('--primary-color', "#468189");
            setColorVariable('--secondary-color', "#d49a6a");
            setColorVariable('--tertiary-color', "#1d1d1d");
            setColorVariable('--bcgrd', "#f5f5f5");
            // logo.src = "../images/ReColorlight.png";
        }
    }

    // Call the function to set the initial theme
    dark_light_mode();

    const darkModeToggle = document.getElementById("theme-switch");

    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'true') {
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener("change", function () {
        localStorage.setItem('darkMode', this.checked ? 'true' : 'false');
        dark_light_mode();  // Update the colors when the toggle changes
    });

});
