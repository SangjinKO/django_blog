const FIREBASE_config = {
    apiKey: "AIzaSyA3x6DTbj3_X13SUAtmXXOd19k1KcMZvJo",
    authDomain: "spartaproject-86d31.firebaseapp.com",
    projectId: "spartaproject-86d31",
    storageBucket: "spartaproject-86d31.appspot.com",
    messagingSenderId: "555159039220",
    appId: "1:555159039220:web:0f68fae62961c00cb2c2a1",
    measurementId: "G-MFRT6YGBSM"
    }

const SAVEKEY = "sangjinko"
var date = new Date();
var date = new Date(date.setDate(date.getDate()-7));
var year = date.getFullYear();
var month = ("0" + (1 + date.getMonth())).slice(-2);
var day = ("0" + date.getDate()).slice(-2);
const LASTDAY = year + month + day;
const LASTDAY_disp = year + "-" + month + "-" + day;

// const MOVIEAPI_config = {
//     URL: "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=d92f213c5c48e942e1aab0de7bd76775&itemPerPage=3&targetDt=" + LASTDAY 
//     }
