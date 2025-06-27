import "../styles/globals.css";
import "../components/home/Loading.css"; // Import the CSS file for loading styles
import { AppProps } from "next/app";
import React, { useState, useEffect } from "react";
import Loading from "../components/home/Loading";
import { AuthProvider } from "../contexts/AuthContext";

function MyApp({ Component, pageProps }: AppProps) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate a loading delay
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000); // Adjust the delay as needed

    return () => clearTimeout(timer);
  }, []);

  return (
    <AuthProvider>
      {isLoading ? <Loading /> : <Component {...pageProps} />}
    </AuthProvider>
  );
}

export default MyApp;
