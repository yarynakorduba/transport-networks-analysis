const fetch = require("node-fetch");
const {area} = require('@turf/turf')
const fs = require('fs')

const getPolygonOfBristol = () => {const data = fs.readFileSync("../../data/bristol_parsed/bristolPolygon.geojson")
return JSON.parse(data)
}

// lviv oblast "https://raw.githubusercontent.com/EugeneBorshch/ukraine_geojson/master/Lviv.json"

const getPolygonOfLviv = () => console.log("Fetching Lviv polygon...") ||
    fetch("https://raw.githubusercontent.com/kameristov/lvivmaps/master/lvivraions.geojson"
    )
        .then(res => res.json())
        .catch(err => console.log(err));

const compareAreasOfPolygons = async () => {
    const lvivPolygon = await getPolygonOfLviv()
    const bristolPolygon = await getPolygonOfBristol()
    console.log("Lviv area: ", area(lvivPolygon)/1000000)
    console.log("Bristol area: ", area(bristolPolygon)/1000000)
    console.log("Difference: ", area(lvivPolygon)/1000000 - area(bristolPolygon)/1000000)
}

module.exports.getPolygonOfBristol = getPolygonOfBristol
module.exports.getPolygonOfLviv = getPolygonOfLviv
module.exports.compareAreasOfPolygons = compareAreasOfPolygons



