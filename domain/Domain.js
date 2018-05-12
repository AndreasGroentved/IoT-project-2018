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
    getAllTemperatures() {
        return dbx.getAllTemperatures();
    }
    saveTemperature(json) {
        for (let i in json.light) { //Assume all arrays have same size or is corrupt
            const temp = json.temperature[i];
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