const { from, forkJoin} = require("rxjs")
const fs = require("fs")
const turf = require("@turf/turf")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')
const cropDataInPolygon = require("./cropDataInPolygon")
const {getPolygonOfLviv, getPolygonOfBristol} = require('./fetchPolygons')
const {convertJsonToGeojson, convertGeojsonToJson} = require('./jsonGeojsonConverter')
const R = require("ramda")


const VEHICLE_TYPE = "All"
const CITY = "lviv"

const GET_POLYGON = CITY === "lviv" ? getPolygonOfLviv : CITY === "bristol" ? getPolygonOfBristol : null

const filterRedundantStopsFromRoutes = (stopsData, routesData) => {
  const presentStops = stopsData.map(stop => stop.id)
  return  routesData
    .map(route => ({...route, stops: route.stops.filter(stop => presentStops.includes(stop))}))
    .filter(route => route.stops.length > 0)
}


const exploreInitNetworkProperties = () => forkJoin(
  from(readFilePromise("../../data/"+ CITY +"_parsed/initial/" + CITY + VEHICLE_TYPE + "Stops.json")).pipe(
    map(JSON.parse),
    map(convertJsonToGeojson),
    flatMap((stops) => from(cropDataInPolygon(stops, GET_POLYGON))),
    map(convertGeojsonToJson)
  ),
  from(readFilePromise("../../data/"+CITY+"_parsed/initial/" + CITY + VEHICLE_TYPE + "Routes.json")).pipe(
    map(JSON.parse),
  ),
)
  .subscribe(
    ([stops, routes]) => {
        const filtered_routes = filterRedundantStopsFromRoutes(stops, routes)
        const getStopsQuantity = n => n !== 0 && n !== Infinity ? n["stops"].length : n
        const result = {
        "stops": stops.length,
        "max_stops_on_route": R.reduce(R.maxBy(getStopsQuantity), 0, filtered_routes).stops.length,
        "min_stops_on_route": R.reduce(R.minBy(getStopsQuantity), Infinity, filtered_routes).stops.length,
        "mean_stops":
        R.compose(
        result => result/filtered_routes.length,
        R.sum,
        R.map(route => route["stops"].length))(filtered_routes)
        }
        console.log(result)
        return result
    }
  )

exploreInitNetworkProperties()

