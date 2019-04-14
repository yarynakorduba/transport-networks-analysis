const { from, forkJoin} = require("rxjs")
const fs = require("fs")
const turf = require("@turf/turf")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')
const cropDataInPolygon = require("./cropDataInPolygon.js")

const VEHICLE_TYPE = "Bus"

const parseJsonToGeojson = (data) => ({type: "FeatureCollection", features: data.map(stop => ({
  type: "Feature",
  geometry: { type: "Point", coordinates: [stop["lon"], stop["lat"]] },
  properties: { ...stop }
}))})

const convertGeojsonToJson = data => data.features.map(stop => stop.properties)

const clusterWithDbscan = (geoJsonStopsData) => turf.clustersDbscan(geoJsonStopsData, 0.1,
  { mutate: true, minPoints: 2 })

const filterRedundantStopsFromRoutes = (stopsData, routesData) => {
  const presentStops = stopsData.map(stop => stop.id)
  return  routesData
    .map(route => ({...route, stops: route.stops.filter(stop => presentStops.includes(stop))}))
    .filter(route => route.stops.length > 0)
}


forkJoin(
from(readFilePromise("../../data/bristol_parsed/initial/bristol" + VEHICLE_TYPE + "Stops.json")).pipe(
  map(JSON.parse),
  map(parseJsonToGeojson),
  flatMap((stops) => from(cropDataInPolygon(stops))),
  map(clusterWithDbscan),
  map(convertGeojsonToJson)
  ),
  from(readFilePromise("../../data/bristol_parsed/initial/bristol" + VEHICLE_TYPE + "Routes.json")).pipe(
    map(JSON.parse)),
  )
  .subscribe(
    ([stops, routes]) => {
    fs.writeFile("../../data/bristol_parsed/processed/bristolStops" + VEHICLE_TYPE +"Processed.json",
      JSON.stringify(stops), (err) => {
      if (err) throw err
      console.log("The stops file has been saved!")
    })
      fs.writeFile("../../data/bristol_parsed/processed/bristolRoutes" + VEHICLE_TYPE +"Processed.json",
        JSON.stringify(
          filterRedundantStopsFromRoutes(stops, routes)), (err) => {
        if (err) throw err
        console.log("The routes file has been saved!")
      })
  }
)






