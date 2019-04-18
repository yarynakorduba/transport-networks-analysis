const fs = require('fs')
const readFilePromise = require('./readFilePromise')
const { from} = require("rxjs")
const turf = require("@turf/turf")
const { map, flatMap } = require("rxjs/operators")
const cropDataInPolygon = require("./cropDataInPolygon")
const {getPolygonOfLviv, getPolygonOfBristol} = require('./fetchPolygons')
const {convertJsonToGeojson} = require('./jsonGeojsonConverter')
const R = require("ramda")

const VEHICLE_TYPE = "All"
const CITY = "lviv"
const GET_POLYGON = CITY === "lviv" ? getPolygonOfLviv : CITY === "bristol" ? getPolygonOfBristol : null


const calculateDistances = (data) => R.compose(
  R.filter(n => n !== 0),
  R.sort((a,b) => a-b),
  R.flatten,
    R.map(
      source_stop => data.features.map(
        target_stop => turf.distance(source_stop, target_stop)
      )
    ),
  )(data.features)

const findStopsDistances = () => {
  from(readFilePromise("../../data/"+ CITY +"_parsed/initial/" + CITY + VEHICLE_TYPE + "Stops.json")).pipe(
    map(JSON.parse),
    map(convertJsonToGeojson),
    flatMap((stops) => from(cropDataInPolygon(stops, GET_POLYGON))),
    map(calculateDistances)
  ).subscribe(
    (distances) => {
      console.log(distances)
      fs.writeFile("../../data/"+ CITY +"_parsed/clustering_test/"+ CITY + VEHICLE_TYPE +"StopsDistances.json",
        JSON.stringify(distances), (err) => {
          if (err) throw err
          console.log("The stops file has been saved!")
        })
    })
}

findStopsDistances()