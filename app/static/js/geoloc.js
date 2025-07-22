navigator.geolocation.getCurrentPosition(function(position) {
  fetch("/api/ubicacion", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      lat: position.coords.latitude,
      lng: position.coords.longitude
    })
  });
});
