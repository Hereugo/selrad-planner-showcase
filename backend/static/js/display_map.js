const locations = JSON.parse(document.getElementById("locations").textContent);

const features = [];
for (let i = 0; i < locations.length; i++) {
  features.push(
    new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([
          parseFloat(locations[i].lon),
          parseFloat(locations[i].lat),
        ]),
      ),
    }),
  );
}

const vectorSource = new ol.source.Vector({
  features: features,
});

const vectorLayer = new ol.layer.Vector({
  source: vectorSource,
  style: new ol.style.Style({
    image: new ol.style.Circle({
      radius: 8,
      fill: new ol.style.Fill({ color: "red" }),
      stroke: new ol.style.Stroke({
        color: "white",
        width: 2,
      }),
    }),
  }),
});

const map = new ol.Map({
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM(),
    }),
    vectorLayer,
  ],
  target: "map",
  view: new ol.View({
    center: [0, 0],
    zoom: 2,
  }),
});
