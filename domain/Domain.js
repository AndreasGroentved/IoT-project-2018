"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Database_1 = require("../data/Database");
const Node_1 = require("./Node");
let dbx;
class Domain {
    constructor() {
        dbx = new Database_1.Database();
    }
    test() {
        return "nailed it";
    }
    getTemperatures(from, to) {
        return dbx.getTemperatures(from, to);
    }
    getAllTemperatures() {
        return dbx.getAllTemperatures();
    }
    saveTemperature(json) {
        console.log("sup");
        console.log("woot");
        console.log(json);
        // json = json.substring(1, json.length - 1);
        // json = JSON.parse(json);
        console.log(json);
        console.log(json.light);
        for (let i in json.light) { //Assume all arrays have same size or is corrupt
            console.log("loop");
            const temp = json.temp[i];
            const light = json.light[i];
            const id = json.id;
            const time = json.time[i];
            console.log("id " + id);
            //let node:Node = JSON.parse(json);
            const node = new Node_1.Node(temp, light, time, id);
            console.log(node);
            dbx.saveTemperature(node);
        }
    }
}
exports.Domain = Domain;
//# sourceMappingURL=Domain.js.map