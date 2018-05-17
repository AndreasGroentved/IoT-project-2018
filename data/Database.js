"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Node_1 = require("../domain/Node");
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
                let nodes = [];
                snapshot.forEach((doc) => {
                    if (doc.val().temperature != null) {
                        let tempNode = new Node_1.Node(doc.val().temperature, doc.val().light, doc.val().time, doc.val().id);
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
    saveTemperature(node) {
        console.log("save");
        firebase.database().ref('Temperatures/').push({
            temperature: node.temperature,
            time: node.time,
            light: node.light,
            id: node.id
        }).then(function (val) {
            console.log(val);
        });
    }
}
exports.Database = Database;
//# sourceMappingURL=Database.js.map