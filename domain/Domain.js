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
    test2() {
        dbx.test();
    }
}
exports.Domain = Domain;
//# sourceMappingURL=Domain.js.map