const fs = require("fs")
const { from, forkJoin} = require("rxjs")
const { map, flatMap } = require("rxjs/operators")
const readFilePromise = require('./readFilePromise')

const arrayReducer = (accumulator, currentValue) => accumulator.concat(currentValue);

const mergeDatasets = (datasets) => datasets.reduce(arrayReducer, [] )


forkJoin(from(readFilePromise("../../data/bristol_parsed/initial/bristolBusStops.json")).pipe(
  map(JSON.parse)),
  from(readFilePromise("../../data/bristol_parsed/initial/bristolCoachStops.json")).pipe(
  map(JSON.parse)),
  from(readFilePromise("../../data/bristol_parsed/initial/bristolTrainStops.json")).pipe(
  map(JSON.parse))
  ).subscribe(
    ([busStops, coachStops, trainStops]) => {
    fs.writeFile("../../data/bristol_parsed/initial/bristolAllStops.json",
      JSON.stringify(mergeDatasets([busStops, coachStops, trainStops])), (err) => {
      if (err) throw err
      console.log("The all stops file has been saved!")
    })
  }
)

forkJoin(from(readFilePromise("../../data/bristol_parsed/initial/bristolBusRoutes.json")).pipe(
  map(JSON.parse)),
  from(readFilePromise("../../data/bristol_parsed/initial/bristolCoachRoutes.json")).pipe(
  map(JSON.parse)),
  from(readFilePromise("../../data/bristol_parsed/initial/bristolTrainRoutes.json")).pipe(
  map(JSON.parse))
  ).subscribe(
    ([busStops, coachStops, trainStops]) => {
    fs.writeFile("../../data/bristol_parsed/initial/bristolAllRoutes.json",
      JSON.stringify(mergeDatasets([busStops, coachStops, trainStops])), (err) => {
      if (err) throw err
      console.log("The all routes file has been saved!")
    })
  }
)