const { from, forkJoin} = require("rxjs")
const fs = require("fs")
const turf = require("@turf/turf")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')
const cropDataInPolygon = require("./cropDataInPolygon")
const cropGeoDataInRadius = require('./cropDataInTheRadius')
const {getPolygonOfLviv, getPolygonOfBristol} = require('./fetchPolygons')
const {convertJsonToGeojson, convertGeojsonToJson} = require('./jsonGeojsonConverter')
const R = require("ramda")


const GET_LVIV_POLYGON = getPolygonOfLviv
const GET_BRISTOL_POLYGON = getPolygonOfBristol

const filterRedundantStopsFromRoutes = (stopsData, routesData) => {
  const presentStops = stopsData.map(stop => stop.id)
  return  routesData
    .map(route => ({...route, stops: route.stops.filter(stop => presentStops.includes(stop))}))
    .filter(route => route.stops.length > 0)
}

const getCentroid = geoJsonStopsData => turf.centroid(geoJsonStopsData);
const getCenterOfMass = geoJsonStopsData => turf.centerOfMass(geoJsonStopsData);
const getCenter = geoJsonStopsData => turf.center(geoJsonStopsData);

const countStopsForDifferentRadius = (stopsGeojson) => {
    const radiusArray = Array(1800).fill(0).map((e,i)=>(i+1)/100) //km
    const centroid = getCenter(stopsGeojson)
    console.log(getCentroid(stopsGeojson))
    console.log(getCenterOfMass(stopsGeojson))
    console.log(turf.center(stopsGeojson))
    return R.fromPairs(radiusArray.map(radius =>
     [""+radius, cropGeoDataInRadius(stopsGeojson, centroid, radius).features.length]))
}


const exploreInitNetworkProperties = () => forkJoin(
  from(readFilePromise("../../data/lviv_parsed/initial/lvivAllStops.json")).pipe(
    map(JSON.parse),
    map(convertJsonToGeojson),
    flatMap((stops) => from(cropDataInPolygon(stops, GET_LVIV_POLYGON))),
    map(countStopsForDifferentRadius)
  ),
    from(readFilePromise("../../data/bristol_parsed/initial/bristolAllStops.json")).pipe(
    map(JSON.parse),
    map(convertJsonToGeojson),
    flatMap((stops) => from(cropDataInPolygon(stops, GET_BRISTOL_POLYGON))),
    map(countStopsForDifferentRadius)
  )
)
  .subscribe(
    ([lvivStops, bristolStops]) => {
         fs.writeFile("../../data/lviv_parsed/initial/lvivStopsOnRadiusAroundCentroidDependence.json",
        JSON.stringify(lvivStops), (err) => {
          if (err) throw err
          console.log("The stops file has been saved!")
        })
      fs.writeFile("../../data/bristol_parsed/initial/bristolStopsOnRadiusAroundCentroidDependence.json",
              JSON.stringify(bristolStops), (err) => {
          if (err) throw err
          console.log("The routes file has been saved!")
        })
    }
  )

module.exports.countStopsForDifferentRadius = countStopsForDifferentRadius