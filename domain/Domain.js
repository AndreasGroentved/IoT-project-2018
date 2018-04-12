"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Database_1 = require("../data/Database");
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
        console.log("save yo");
        const temperature = json.temperature;
        const time = json.time;
        console.log("temp " + temperature + ", time " + time);
        dbx.saveTemperature(temperature, time);
    }
}
exports.Domain = Domain;
//# sourceMappingURL=Domain.js.map