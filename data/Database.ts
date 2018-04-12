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

export class Database {
    constructor() {

    }


    test(res) {

        firebase.database().ref('/Temperatures').once('value')
            .then((snapshot) => {
                snapshot.forEach((doc) => {

                    console.log(doc.id, '=>', doc.data());
                    res.render('index', {title: doc.date()});
                });
            })
            .catch((err) => {
                console.log('Error getting documents', err);
            });


    }

}
