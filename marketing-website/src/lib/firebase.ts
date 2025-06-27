// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCFNiLtIsHNd-hqGCL_y1ZL3wOUfaZTD5w",
  authDomain: "qualitrackweb.firebaseapp.com",
  projectId: "qualitrackweb",
  storageBucket: "qualitrackweb.firebasestorage.app",
  messagingSenderId: "709031457935",
  appId: "1:709031457935:web:6be92f8e216dc1dae7ecfa",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
