import './App.css';
import {searchHotels} from "../utils/hotel_search";
import HotelResults from "./HotelResults";
import {RequestStatus} from "../schema/enums";

import { useState } from "react"


const HotelBrowser = (props: any) => {

  const {switchToHotel} = props;

  const [editHotelCountry, setEditHotelCountry] = useState('');
  const [editHotelCity, setEditHotelCity] = useState('');

  const [searchStatus, setSearchStatus] = useState<RequestStatus>("initialized");
  const [searchResults, setSearchResults] = useState([]);

  const trySearchHotels = (city: string, country: string) => {

    if (city && country) {

      setSearchStatus("in_flight")

      const callback = (results: any) => {
        setSearchResults(results);
        setSearchStatus("completed");
      }

      const errback = () => {
        setSearchStatus("errored");
        console.log("ERROR!");
      }

      searchHotels(city, country, callback, errback)

    }
    
  }

  return (
    <div>
      <p>
        Country:
          <input
            className="inlineInput"
            type="text"
            name="hotel_country"
            value={editHotelCountry}
            onChange={(e) => setEditHotelCountry(e.target.value.toUpperCase())}
            onKeyPress={(e) => {if (e.key === 'Enter') { trySearchHotels(editHotelCountry, editHotelCity) }}}
          />
        </p>
      <p>
        City:
          <input
            className="inlineInput"
            type="text"
            name="hotel_city"
            value={editHotelCity}
            onChange={(e) => setEditHotelCity(e.target.value)}
            onKeyPress={(e) => {if (e.key === 'Enter') { trySearchHotels(editHotelCountry, editHotelCity) }}}
          />
      </p>
      <button
        onClick={() => trySearchHotels(editHotelCountry, editHotelCity)}
      >
        Search
      </button>
      <button
        onClick={() => {
          setEditHotelCountry("");
          setEditHotelCity("");
          setSearchStatus("initialized");
          setSearchResults([]);
        }}
      >
        Reset
      </button>
      <HotelResults
        searchStatus={searchStatus}
        searchResults={searchResults}
        switchToHotel={switchToHotel}
      />
    </div>
  );
}

export default HotelBrowser
