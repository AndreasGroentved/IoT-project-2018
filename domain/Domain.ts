import {Database} from "../data/Database";
import {Node} from "./Node";

let dbx;

export class Domain {

    constructor() {
        dbx = new Database();
    }

    test() {
        return "nailed it";
    }

    getAllTemperatures(): Promise<Node[]> {
        return dbx.getAllTemperatures();
    }

    saveTemperature(json) {
        console.log("sup");
        json = JSON.parse(json);
        console.log(json.light);
        for (let i in json.light) {//Assume all arrays have same size or is corrupt
            console.log("loop");
            const temp = json.temperature[i];
            const light = json.light[i];
            const id = json.id;
            const time = json.time[i];
            console.log("id " + id);
            //let node:Node = JSON.parse(json);
            const node: Node = new Node(temp, light, time, id);
            console.log(node);
            dbx.saveTemperature(node);
        }
    }

}