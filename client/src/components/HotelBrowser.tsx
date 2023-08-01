import './App.css';
import {searchHotels} from "../utils/hotel_search";
import HotelResults from "./HotelResults";
// import {UserDesc} from "../interfaces/interfaces";

import { /*useEffect,*/ useState } from "react"


const HotelBrowser = () => {

  const [editHotelCountry, setEditHotelCountry] = useState('');
  const [editHotelCity, setEditHotelCity] = useState('');

  const [searchStatus, setSearchStatus] = useState(0); // 0=no search, 1=running, 2=results are there
  const [searchResults, setSearchResults] = useState([]);

  const trySearchHotels = (city: string, country: string) => {


    if (city && country) {

      setSearchStatus(1)

      const fake_callback = (results: any) => {
        setSearchResults(results.data);
        setSearchStatus(2);
      }

      const err_back = () => {
        // setSearchStatus(3);
        console.log("ERROR!");
      }

      searchHotels(city, country, fake_callback, err_back)

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
            // onKeyPress={(e) => {if (e.key === 'Enter') { trySetUserId(editUserId) }}}
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
            // onKeyPress={(e) => {if (e.key === 'Enter') { trySetUserId(editUserId) }}}
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
          setSearchStatus(0);
          setSearchResults([]);
        }}
      >
        Reset
      </button>
      <HotelResults
        searchStatus={searchStatus}
        searchResults={searchResults}
      />
    </div>
  );
}

export default HotelBrowser
