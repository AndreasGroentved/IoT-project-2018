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
        const temp = json.temperature;
        const light = json.light;
        const id = json.id;
        const time = json.time;
        //let node:Node = JSON.parse(json);
        const node: Node = new Node(temp, light, time, id);
        console.log(node);
        dbx.saveTemperature(node);
    }

}