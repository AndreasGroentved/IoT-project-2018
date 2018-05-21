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

    getTemperatures(from, to) {
        return dbx.getTemperatures(from, to);
    }

    getAllTemperatures(): Promise<Node[]> {
        return dbx.getAllTemperatures();
    }

    saveTemperature(json) {
        console.log(json);

        for (let i in json.light) {//Assume all arrays have same size or is corrupt
            console.log("loop");
            const temp = json.temp[i];
            const light = json.light[i];
            const id = json.id;
            const time = json.time[i];
            const node: Node = new Node(temp, light, time, id);
            console.log(node);
            dbx.saveTemperature(node);
        }
    }

}