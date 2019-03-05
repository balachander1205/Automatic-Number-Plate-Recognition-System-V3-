/*!
 * jQuery.gMapping.js
 *
 * Copyright 2017, MONSTER DIVE Inc.
 * Released under the MIT license
 *
 * Date: 2017-03-25
 */
(function (factory) {
  if (typeof module === "object" && typeof module.exports === "object") {
    module.exports = factory(require("jquery"), window, document);
  } else {
    factory(jQuery, window, document);
  }
}(function ($, window, document, undefined) {
  return $.fn.gMapping = function (lat, lng, options) {
    var latlng = new google.maps.LatLng(lat, lng);

    // set default options
    options = $.extend({
      center: latlng,
      zoom: 17
    }, options);

    var map = new google.maps.Map(this[0], options);

    // set color
    var styles;
    var styledMapType;

    if (options.color) {
      styles = [
        {
          stylers: [
            { hue: options.color.hue ? options.color.hue : '' },
            { saturation: options.color.saturation ? options.color.saturation : 0 },
            { lightness: options.color.lightness ? options.color.lightness : 0 }
          ]
        }
      ];

      styledMapType = new google.maps.StyledMapType(styles, { name: 'custom' });
      map.mapTypes.set('custom', styledMapType);
      map.setMapTypeId('custom');
    }

    // set marker
    var markerOptions = {
      position: latlng,
      map: map,
    };

    if (options.marker && options.marker.url) {
      var icon = { url: options.marker.url };
      options.marker.anchor && (icon.anchor = new google.maps.Point(options.marker.anchor[0], options.marker.anchor[1]));
      options.marker.size && (icon.scaledSize = new google.maps.Size(options.marker.size[0], options.marker.size[1]));
      markerOptions.icon = icon;
    }

    var marker = new google.maps.Marker(markerOptions);
  };
}));
