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
    getTemperatures(from, to) {
        return dbx.getTemperatures(from, to);
    }
    saveTemperature(json) {
        const temp = json.temperature;
        const light = json.light;
        const id = json.id;
        const time = json.time;
        //let node:Node = JSON.parse(json);
        const node = new Node_1.Node(temp, light, time, id);
        console.log(node);
        dbx.saveTemperature(node);
    }
}
exports.Domain = Domain;
//# sourceMappingURL=Domain.js.map