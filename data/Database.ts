import {Node} from "../domain/Node";

let firebase = require('firebase');

const config = {
    apiKey: "AIzaSyAAaoGd7pd77x52d2sO-NPmH3buLRS-sTk",
    authDomain: "iot-project-5e6fb.firebaseapp.com",
    databaseURL: "https://iot-project-5e6fb.firebaseio.com",
    storageBucket: "iot-project-5e6fb.appspot.com",
};
firebase.initializeApp(config);

export class Database {
    constructor() {

    }

    getAllTemperatures(): Promise<Node[]> {
        return new Promise<Node[]>((resolve) => {
            console.log("yolo");
            firebase.database().ref('/Temperatures/').once('value')
                .then((snapshot) => {
                    let nodes: Array<Node> = [];
                    snapshot.forEach((doc) => {
                        if (doc.val().temperature != null) {
                            let tempNode: Node = new Node(doc.val().temperature, doc.val().light, doc.val().time, doc.val().id);
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

    getTemperatures(from, to) {
        return new Promise((resolve) => {
            console.log("getTemperatures between " + from + " and " + to);
            firebase.database().ref('/Temperatures/').once('value')
                .then((snapshot) => {
                    let nodes = [];
                    snapshot.forEach((doc) => {
                        if (doc.val().temperature != null && (doc.val().time != null && doc.val().time > from && doc.val().time < to)) {
                            let tempNode = new Node(doc.val().temperature, doc.val().light, doc.val().time, doc.val().id);
                            // console.log(tempNode);
                            nodes.push(tempNode);
                        }
                    });
                    // console.log(nodes);
                    resolve(nodes);
                })
                .catch((err) => {
                    console.log('Error getting documents', err);
                });
        });
    }


    saveTemperature(node: Node) {
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
