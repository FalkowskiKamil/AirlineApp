
function changeTheme() {
    // Pobierz bieżące wartości zmiennych CSS
    const currentBackground = getComputedStyle(document.documentElement).getPropertyValue('--background').trim();
    
    // Sprawdź aktualne wartości i przełączaj się między dwiema zestawami
    if (currentBackground === 'rgb(255, 255, 255)') {
      // Jeśli obecne tło jest białe, zmień na czarne
      document.documentElement.style.setProperty('--background', 'rgb(0, 0, 0)');
      document.documentElement.style.setProperty('--text', 'rgb(255, 255, 255)');
      document.documentElement.style.setProperty('--border', 'rgb(44, 44, 44)');
      document.documentElement.style.setProperty('--background-image', 'url("background_night.png")')
    } else {
      // W przeciwnym razie zmień na białe
      document.documentElement.style.setProperty('--background', 'rgb(255, 255, 255)');
      document.documentElement.style.setProperty('--text', 'rgb(0, 0, 0)');
      document.documentElement.style.setProperty('--border', 'rgb(211, 211, 211)');
      document.documentElement.style.setProperty('--background-image', 'url("background.png")')
    }
    // Możesz także dodać kod do obsługi innych zmiennych
  }