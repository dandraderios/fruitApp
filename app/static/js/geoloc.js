function enviarUbicacion() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const data = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      await fetch('/api/ubicacion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    });
  } else {
    console.log("Geolocalización no disponible");
  }
}

function enviarPing() {
  fetch('/api/ping', { method: 'POST' });
}
    function animarAuto() {
      const auto = document.getElementById('auto-icon');
      auto.style.left = 'calc(100% - 40px)';
    }

    function enviarDistanciaKm0() {
      navigator.geolocation.getCurrentPosition(position => {
        fetch('/api/ubicacion/distancia-km0', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
        })
        .then(res => res.json())
        .then(data => {
          console.log(`Distancia calculada desde backend: ${data.distancia_km} km`);
          const distanciaBox = document.getElementById('distancia-box');
          const distanciaText = document.getElementById('distancia-text');
          distanciaText.textContent = `Distancia al km 0 de Santiago: ${data.distancia_km.toFixed(2)} km`;
          distanciaBox.style.display = 'block';

          // Animar auto luego de mostrar la distancia
          setTimeout(animarAuto, 500);
        });
      }, error => {
        alert('No se pudo obtener la ubicación');
      });
    }

// Enviar la ubicación cada 30 segundos
setInterval(enviarUbicacion, 30000); // 30000 ms = 30 segundos

// Enviar el ping cada 5 segundos
setInterval(enviarPing, 5000);

// Enviar inmediatamente al cargar la página
enviarUbicacion();
// Enviar ping inmediatamente al cargar la página
enviarPing();
// Enviar distancia al km 0 inmediatamente al cargar la página
enviarDistanciaKm0();
// También puedes llamar a enviarDistanciaKm0() en un intervalo si es necesario
setInterval(enviarDistanciaKm0, 30000); // 30000 ms =
