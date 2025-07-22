document.addEventListener("DOMContentLoaded", () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async position => {
      const data = {
        lat: position.coords.latitude,
        lon: position.coords.longitude
      };
      await fetch('/ubicacion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    });
  }
});
