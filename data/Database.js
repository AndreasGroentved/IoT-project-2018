"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
let firebase = require('firebase-admin');
const config = {
    apiKey: "AIzaSyAAaoGd7pd77x52d2sO-NPmH3buLRS-sTk",
    authDomain: "iot-project-5e6fb.firebaseapp.com",
    databaseURL: "https://iot-project-5e6fb.firebaseio.com",
    projectId: "iot-project-5e6fb",
    storageBucket: "iot-project-5e6fb.appspot.com",
    messagingSenderId: "460298206239"
};
firebase.initializeApp(config);
class Database {
    constructor() {
    }
    test() {
        firebase.database().ref('/Temperatures/').once('value')
            .then((snapshot) => {
            snapshot.forEach((doc) => {
                console.log(doc.id, '=>', doc.data());
            });
        })
            .catch((err) => {
            console.log('Error getting documents', err);
        });
    }
}
exports.Database = Database;
//# sourceMappingURL=Database.js.map