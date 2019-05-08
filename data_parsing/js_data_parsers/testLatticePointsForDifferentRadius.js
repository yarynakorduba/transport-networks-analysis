const {countStopsForDifferentRadius} = require("./stationsOnRadiusAroundCentroidDependence")
const {polygon, bboxPolygon, pointGrid} = require("@turf/turf")
const fs = require("fs")
const dimension = 30
const bbox = [49.837644, 24.016985, 49.880367, 24.034112]
const testGrid = pointGrid(bbox, cellSide=0.007,  {units: 'kilometers'})

const stops = countStopsForDifferentRadius(testGrid)

fs.writeFile("../../data/pointsInLatticeRadiusAroundCentroidDependence.json",
      JSON.stringify(stops), (err) => {
  if (err) throw err
  console.log("The test file has been saved!")
})