// import { useEffect, useState } from "react"
// import { Dispatch, SetStateAction } from "react";

import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

import './App.css';
import {UserDesc} from "../interfaces/interfaces";

import UserProfileComponent from "./UserProfileComponent";
import HotelBrowser from "./HotelBrowser";
import HotelDetails from "./HotelDetails";


const SiteContents = ({userId}: UserDesc) => {
  return (
    <div className="App-contents">
      <div className="App-navbar">
        { userId && 
          <Router>
            <div>
              <p>
                <Link to="/browse">Browse hotels</Link>
                <Link to="/profile">User profile</Link>
              </p>
            </div>

            <Routes>
              <Route path="/browse" element={<HotelBrowser />} />
              <Route path="/browse/:hotel_id" element={<HotelDetails userId={userId} />} />
              <Route
                path="/profile"
                element={<UserProfileComponent userId={userId} />}
              />
            </Routes>

          </Router>
        }
      </div>
    </div>
  );
}

export default SiteContents
