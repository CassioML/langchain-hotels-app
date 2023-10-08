import { useState } from "react"
// import { Dispatch, SetStateAction } from "react";

import './App.css';
// import {UserDesc} from "../interfaces/interfaces";

import UserProfileComponent from "./UserProfileComponent";
import HotelBrowser from "./HotelBrowser";
import HotelDetails from "./HotelDetails";


const SiteContents = (props: any) => {

  const [currentHotelId, setCurrentHotelId] = useState<string | undefined>(undefined);

  const {userId, currentNavPage, setCurrentNavPage} = props;

  const switchToHotel = (hotel_id: string) => {
    setCurrentHotelId(hotel_id);
    setCurrentNavPage("hotel_details");
  };

  return (
    <div className="App-contents">
      <div className="App-navbar">
        { userId && <>
          <div>
            <span onClick={() => setCurrentNavPage("hotel_search")}>Browse hotels</span>
            <span onClick={() => setCurrentNavPage("user_preferences")}>User profile</span>
          </div>

          { currentNavPage === "hotel_search" && <>
            <HotelBrowser switchToHotel={switchToHotel}/>
          </>}

          { currentNavPage === "hotel_details" && <>
            <HotelDetails userId={userId} hotelId={currentHotelId} />
          </>}

          { currentNavPage === "user_preferences" && <>
            <UserProfileComponent userId={userId} />
          </>}

          { currentNavPage === "login" && <>
            <p>LOGIN</p>
          </>}

        </> }
      </div>
    </div>
  );
}

export default SiteContents
