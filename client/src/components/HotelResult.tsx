import './App.css';

import { useEffect, useState } from "react";
import {Link} from "react-router-dom";

import {RequestStatus} from "../interfaces/interfaces";

import {baseHotelSummary} from "../utils/hotel_search";

const HotelResult = (props: any) => {

  const [summaryStatus, setSummaryStatus] = useState<RequestStatus>("initialized");
  const [hotelSummary, setHotelSummary] = useState<string | undefined>(undefined);

  const {hotel} = props;

  useEffect(
    () => {
      console.log(`getting the summary for ${hotel.id}`);
      setSummaryStatus("in_flight")

      const callback = (results: any) => {
        setHotelSummary(results.summary);
        setSummaryStatus("completed");
      }

      const err_back = () => {
        setSummaryStatus("errored");
        console.log("ERROR (baseHotelSummary)!");
      }

      baseHotelSummary(hotel, hotel.id, callback, err_back);
    },
    [hotel]
  );

  if (hotelSummary){
    return <li key={hotel.id}>
      <Link to={`/browse/${hotel.id}`}>
        {`${hotel.name} (${hotel.id}):`} <b>{hotelSummary}</b>
      </Link>
    </li>;
  }else{
    return <li key={hotel.id}>
      <Link to={`/browse/${hotel.id}`}>
        {`${hotel.name} (${hotel.id})`} [...]
      </Link>
    </li>;
  }
}

export default HotelResult
