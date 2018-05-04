import {Database} from "../data/Database";
import {TempNode} from "./TempNode";

let dbx;

export class Domain {

    constructor() {
        dbx = new Database();
    }

    test() {
        return "nailed it";
    }

    getAllTemperatures(): Promise<TempNode[]> {
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