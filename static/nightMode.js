let theme = localStorage.getItem("theme");

function changeTheme() {
    if (theme ==="dark") {
      document.documentElement.style.setProperty('--background', 'rgb(255, 255, 255)');
      document.documentElement.style.setProperty('--background-image', 'url("background.png")');
      document.documentElement.style.setProperty('--banner-text-color', 'rgb(20, 45, 76)');
      document.documentElement.style.setProperty('--border', 'rgb(211, 211, 211)');
      document.documentElement.style.setProperty('--dark-mode-image', 'url("night-mode-button.png"');
      document.documentElement.style.setProperty('--navi-text-color', 'rgb(13, 110, 253)');
      document.documentElement.style.setProperty('--text', 'rgb(0, 0, 0)');
      document.querySelector("body").classList.remove("dark");
      document.querySelector("body").classList.add("light");
      theme = "light"
    } else {
      document.documentElement.style.setProperty('--background', 'rgb(0, 0, 0)');
      document.documentElement.style.setProperty('--background-image', 'url("background_night.png")');
      document.documentElement.style.setProperty('--banner-text-color', 'rgb(53, 116, 194)');
      document.documentElement.style.setProperty('--border', 'rgb(44, 44, 44)');
      document.documentElement.style.setProperty('--dark-mode-image', 'url("night-mode-button-night.png"');
      document.documentElement.style.setProperty('--navi-text-color', 'rgb(13, 110, 253)');
      document.documentElement.style.setProperty('--text', 'rgb(255, 255, 255)');
      document.querySelector("body").classList.remove("light");
      document.querySelector("body").classList.add("dark");
      theme = "dark"
    }
    localStorage.setItem("theme", theme);
  }

  
if (theme === "dark") {
  document.querySelector("body").classList.add("dark");
  document.querySelector("body").classList.remove("light");
  document.documentElement.style.setProperty('--background', 'rgb(0, 0, 0)');
  document.documentElement.style.setProperty('--background-image', 'url("background_night.png")');
  document.documentElement.style.setProperty('--banner-text-color', 'rgb(53, 116, 194)');
  document.documentElement.style.setProperty('--border', 'rgb(44, 44, 44)');
  document.documentElement.style.setProperty('--dark-mode-image', 'url("night-mode-button-night.png"');
  document.documentElement.style.setProperty('--navi-text-color', 'rgb(13, 110, 253)');
  document.documentElement.style.setProperty('--text', 'rgb(255, 255, 255)');

}

if (theme === "light") {
  document.querySelector("body").classList.add("light");
  document.querySelector("body").classList.remove("dark");
  document.documentElement.style.setProperty('--background', 'rgb(255, 255, 255)');
  document.documentElement.style.setProperty('--background-image', 'url("background.png")');
  document.documentElement.style.setProperty('--banner-text-color', 'rgb(20, 45, 76)');
  document.documentElement.style.setProperty('--border', 'rgb(211, 211, 211)');
  document.documentElement.style.setProperty('--dark-mode-image', 'url("night-mode-button.png"');
  document.documentElement.style.setProperty('--navi-text-color', 'rgb(13, 110, 253)');
  document.documentElement.style.setProperty('--text', 'rgb(0, 0, 0)');
}