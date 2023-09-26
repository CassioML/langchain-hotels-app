import { useState } from "react"
// import { Dispatch, SetStateAction } from "react";

import './App.css';
// import {UserDesc} from "../interfaces/interfaces";

import UserProfileComponent from "./UserProfileComponent";
import HotelBrowser from "./HotelBrowser";
import HotelDetails from "./HotelDetails";


const SiteContents = (props: any) => {

  const [currentHotelId, setCurrentHotelId] = useState<string | undefined>(undefined);

  const {userId, currentUserPage, setCurrentUserPage} = props;

  const switchToHotel = (hotel_id: string) => {
    setCurrentHotelId(hotel_id);
    setCurrentUserPage("hotel_details");
  };

  return (
    <div className="App-contents">
      <div className="App-navbar">
        { userId && <>
          <div>
            <span onClick={() => setCurrentUserPage("hotel_search")}>Browse hotels</span>
            <span onClick={() => setCurrentUserPage("user_profile")}>User profile</span>
          </div>

          { currentUserPage === "hotel_search" && <>
            <HotelBrowser switchToHotel={switchToHotel}/>
          </>}

          { currentUserPage === "hotel_details" && <>
            <HotelDetails userId={userId} hotelId={currentHotelId} />
          </>}

          { currentUserPage === "user_profile" && <>
            <UserProfileComponent userId={userId} />
          </>}

        </> }
      </div>
    </div>
  );
}

export default SiteContents
