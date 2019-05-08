const { from, forkJoin} = require("rxjs")
const fs = require("fs")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')
const cropDataInPolygon = require("./cropDataInPolygon")
const {getPolygonOfLviv, getPolygonOfBristol} = require('./fetchPolygons')
const {convertJsonToGeojson, convertGeojsonToJson} = require('./jsonGeojsonConverter')
const R = require("ramda")

const filterJourneys = journeys => R.uniq(journeys)

const groupByRouteIdDirectionHolidays = route => route.id + "_" + route.direction + "_" + route.bankHolidays
const stopsLength = n => n !== 0 ? n.stops.length : n;


// DANGEROUS!!! Use only if you are sure that no routes with the same name
// in the dataset are different by default

const convertJourneysToRoutes = (city, vehicle_type) =>
  from(readFilePromise("../../data/"+city+"_parsed/initial/" + city + vehicle_type + "Routes.json")).pipe(
    map(JSON.parse),
    map(filterJourneys),
    map(R.groupBy(groupByRouteIdDirectionHolidays)),
    map(R.values),
    map(R.map(value => R.reduce(R.maxBy(stopsLength), 0, value)))
    ).subscribe(routes => {
        fs.writeFile("../../data/"+city+"_parsed/processed/"+ city + vehicle_type +"uniqueRoutes.json",
        JSON.stringify(routes), (err) => {
          if (err) throw err
          console.log("The filtered routes file has been saved!")
        })
    })

convertJourneysToRoutes("lviv", "all")