import {Database} from "../data/Database";

let dbx;

export class Domain {

    constructor() {
        dbx = new Database();
    }

    test(){
        return "nailed it";
    }

    test2(){
        dbx.test();
    }

}