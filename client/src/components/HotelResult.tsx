import './App.css';

import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

import {RequestStatus} from "../interfaces/enums";

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

      const errback = () => {
        setSummaryStatus("errored");
        console.log("ERROR (baseHotelSummary)!");
      }

      baseHotelSummary(hotel, hotel.id, callback, errback);
    },
    [hotel]
  );

  return <li key={hotel.id}>
    <Link to={`/browse/${hotel.id}`}>
      {`${hotel.name} (${hotel.id}):`}
        { (summaryStatus === "initialized" || summaryStatus === "in_flight") &&
          <span>...</span>
        }
        { (summaryStatus === "completed") &&
          <b>{hotelSummary || "(no summary)"}</b>
        }
        { (summaryStatus === "errored") &&
          <span>(could not get hotel summary)</span>
        }
    </Link>
  </li>;

}

export default HotelResult
