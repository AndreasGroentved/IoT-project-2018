"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const TempNode_1 = require("../domain/TempNode");
let firebase = require('firebase');
const config = {
    apiKey: "AIzaSyAAaoGd7pd77x52d2sO-NPmH3buLRS-sTk",
    authDomain: "iot-project-5e6fb.firebaseapp.com",
    databaseURL: "https://iot-project-5e6fb.firebaseio.com",
    storageBucket: "iot-project-5e6fb.appspot.com",
};
firebase.initializeApp(config);
class Database {
    constructor() {
    }
    getAllTemperatures() {
        return new Promise((resolve) => {
            console.log("yolo");
            firebase.database().ref('/Temperatures/').once('value')
                .then((snapshot) => {
                var nodes = [];
                snapshot.forEach((doc) => {
                    if (doc.val().temperature != null) {
                        let tempNode = new TempNode_1.TempNode(doc.val().temperature, doc.val().time);
                        console.log(tempNode);
                        nodes.push(tempNode);
                    }
                });
                console.log(nodes);
                resolve(nodes);
            })
                .catch((err) => {
                console.log('Error getting documents', err);
            });
        });
    }
    saveTemperature(temperature, time) {
        console.log("save");
        firebase.database().ref('Temperatures/').push({
            temperature: temperature,
            time: time
        }).then(function (val) {
            console.log(val);
        });
    }
}
exports.Database = Database;
//# sourceMappingURL=Database.js.map