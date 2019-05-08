const fs = require('fs')
const turf = require('@turf/turf')
const {calculateDistances} = require('./allStopsDistances.js')
const R = require('ramda')
const readFilePromise = require('./readFilePromise')
const {convertJsonToGeojson} = require('./jsonGeojsonConverter.js')
const { map, flatMap } = require("rxjs/operators")
const { from, forkJoin} = require("rxjs")


const RADIUS = 40 //m
const CITY = "bristol"
const VEHICLE_TYPE = "All"

const getClusterCounts = (filename="../../data/" + CITY + "_parsed/processed/"
        + CITY + VEHICLE_TYPE +"StopsProcessed"+RADIUS+"m.json") => {

    from(readFilePromise(filename)).pipe(
        map(JSON.parse),
        map(convertJsonToGeojson),
        map(geoData => {
        let results = []
        turf.clusterEach(geoData,
            'cluster', function (cluster, clusterValue, currentIndex) {
                if (cluster) {
                    const newVal = R.pipe(
                    calculateDistances,
                   R.flatten,
                   data => Math.max(...data),
                   )(cluster)
                   results = results.concat(
                   newVal
                   )
                   }

                   })

                   return results
                   }
                ),
        map(R.sort((a,b) => a-b))
                )
    .subscribe(
    (results) => {
          fs.writeFile("../../data/"+ CITY +"_parsed/clustering_test/"+
           CITY +"MaxStopsDistancesInClusters" + RADIUS + "m.json",
            JSON.stringify(results), (err) => {
          if (err) throw err
          console.log("The max cluster stops stops file has been saved!")
        })
    })
}

module.exports = getClusterCounts

getClusterCounts()