import {TempNode} from "../domain/TempNode";

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

    getAllTemperatures(): Promise<TempNode[]> {
        return new Promise<TempNode[]>((resolve) => {
            console.log("yolo");
            firebase.database().ref('/Temperatures/').once('value')
                .then((snapshot) => {
                    var nodes: Array<TempNode> = [];
                    snapshot.forEach((doc) => {
                        if (doc.val().temperature != null) {
                            let tempNode: TempNode = new TempNode(doc.val().temperature, doc.val().time);
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


    saveTemperature(temperature: number, time: Number) {
        console.log("save");
        firebase.database().ref('Temperatures/').push({
            temperature: temperature,
            time: time
        }).then(function (val) {
            console.log(val);
        });
    }

}
