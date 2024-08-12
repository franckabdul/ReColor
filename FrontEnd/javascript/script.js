//This will contain the javascript code that is common to all the pages of the website

//There is a bug in the code that is causing the dark mode to not work properly. The bug is that the dark mode is not being saved when the user navigates to a different page. Fix the bug so that the dark mode is saved when the user navigates to a different page.
document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.getElementById("theme-switch");

    function setColorVariable(variableName, value) {
        document.documentElement.style.setProperty(variableName, value);
    }

    function dark_light_mode() {
        const darkMode = localStorage.getItem('darkMode');
        // const logo=document.getElementById("logo");

        if (darkMode === 'true'|| darkMode===null) {
            setColorVariable('--primary-color', "#468189");
            setColorVariable('--secondary-color', "#d49a6a");
            setColorVariable('--tertiary-color', "#faebd7");
            setColorVariable('--bcgrd', "#333131");
            darkModeToggle.checked = true;
            // logo.src = "../images/ReColordark.png";
        } else {
            setColorVariable('--primary-color', "#468189");
            setColorVariable('--secondary-color', "#d49a6a");
            setColorVariable('--tertiary-color', "#1d1d1d");
            setColorVariable('--bcgrd', "#f5f5f5");
            darkModeToggle.checked = false;
            // logo.src = "../images/ReColorlight.png";
        }
    }

    // Call the function to set the initial theme
    window.onload = function () {
        dark_light_mode();
        console.log("Dark mode is set to", localStorage.getItem('darkMode'));
    }


    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'true') {
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener("change", function () {
        localStorage.setItem('darkMode', this.checked ? 'true' : 'false');
        dark_light_mode();  // Update the colors when the toggle changes
    });

});

