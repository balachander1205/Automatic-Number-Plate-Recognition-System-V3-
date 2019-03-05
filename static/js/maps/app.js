$(function () {
  $('#map').gMapping(35.661289, 139.723348, {
    color: {
      hue: '#A02223',
      saturation: 50,
      lightness: 10
    },
    marker: {
      url: 'images/marker.png',
      size: [30, 30],
      anchor: [15, 15]
    }
  });
});