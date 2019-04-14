const fs = require("fs")


const readFilePromise = (fileName) => new Promise((resolve, reject) => {
  fs.readFile(fileName, (err, data) => {
    if (err !== null) return reject(err)
    resolve(data)
  })
})

module.exports = readFilePromise