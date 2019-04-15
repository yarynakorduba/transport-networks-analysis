const { from, forkJoin} = require("rxjs")
const fs = require("fs")
const turf = require("@turf/turf")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')
const cropDataInPolygon = require("./cropDataInPolygon")
const {getPolygonOfLviv, getPolygonOfBristol} = require('./fetchPolygons')

const VEHICLE_TYPE = "Bus"
const CITY = "bristol"
const CLUSTER_RADIUS = 0.03 // km

const GET_POLYGON = CITY === "lviv" ? getPolygonOfLviv : CITY === "bristol" ? getPolygonOfBristol : null

const parseJsonToGeojson = (data) => ({type: "FeatureCollection", features: data.map(stop => ({
  type: "Feature",
  geometry: { type: "Point", coordinates: [stop["lon"], stop["lat"]] },
  properties: { ...stop }
}))})

const convertGeojsonToJson = data => data.features.map(stop => stop.properties)

const clusterWithDbscan = (geoJsonStopsData, km) => turf.clustersDbscan(geoJsonStopsData, km,
  { mutate: true, minPoints: 2 })

const filterRedundantStopsFromRoutes = (stopsData, routesData) => {
  const presentStops = stopsData.map(stop => stop.id)
  return  routesData
    .map(route => ({...route, stops: route.stops.filter(stop => presentStops.includes(stop))}))
    .filter(route => route.stops.length > 0)
}


forkJoin(
from(readFilePromise("../../data/"+ CITY +"_parsed/initial/" + CITY + VEHICLE_TYPE + "Stops.json")).pipe(
  map(JSON.parse),
  map(parseJsonToGeojson),
  flatMap((stops) => from(cropDataInPolygon(stops, GET_POLYGON))),
  map(stops => clusterWithDbscan(stops, CLUSTER_RADIUS)),
  map(convertGeojsonToJson)
  ),
  from(readFilePromise("../../data/"+CITY+"_parsed/initial/" + CITY + VEHICLE_TYPE + "Routes.json")).pipe(
    map(JSON.parse),
    ),
  )
  .subscribe(
    ([stops, routes]) => {
    fs.writeFile("../../data/"+ CITY +"_parsed/processed/"+ CITY + VEHICLE_TYPE +"StopsProcessed"
    + CLUSTER_RADIUS * 1000 +"m.json",
      JSON.stringify(stops), (err) => {
      if (err) throw err
      console.log("The stops file has been saved!")
    })
      fs.writeFile("../../data/"+CITY+"_parsed/processed/"+ CITY + VEHICLE_TYPE +"JourneysProcessed"
      + CLUSTER_RADIUS * 1000 +"m.json",
        JSON.stringify(filterRedundantStopsFromRoutes(stops, routes)), (err) => {
        if (err) throw err
        console.log("The routes file has been saved!")
      })
  }
)






