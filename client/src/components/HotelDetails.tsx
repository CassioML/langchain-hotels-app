import './App.css';

import { useEffect, useState } from "react";

import {customizedHotelDetails} from "../utils/hotel_search";
import {RequestStatus} from "../interfaces/enums";

const HotelDetails = (props: any) => {

  const {userId, hotelId} = props;

  const [hotelDetails, setHotelDetails] = useState<any>();
  const [detailsStatus, setDetailsStatus] = useState<RequestStatus>("initialized");

  useEffect(
    () => {
      console.log(`asking for customized details on ${hotelId} for ${userId}`);
      setDetailsStatus("in_flight")

      const callback = (results: any) => {
        setHotelDetails(results);
        setDetailsStatus("completed");
      }

      const errback = () => {
        setDetailsStatus("errored");
        console.log("ERROR (baseHotelSummary)!");
      }

      customizedHotelDetails(hotelId || "", userId, callback, errback);
    },
    [hotelId, userId]
  );

  return <div>
    { (detailsStatus === "initialized" || detailsStatus === "in_flight") &&
      <div>Getting details ...</div>
    }
    { (detailsStatus === "completed") &&
      <div>
        <div>Details for <b>{hotelDetails.name}</b></div>
        <div>
          <i>Summary: {hotelDetails.summary}</i>
        </div>
        <div>
          <p>Reviews:</p>
          <ul>
            {hotelDetails.reviews.map( (r: any, i: number) =>
              <li key={r.id}>
                <i>{r.title}</i>: {r.body}
              </li>
            )}
          </ul>
        </div>
      </div>
    }
    { (detailsStatus === "errored") &&
      <div>Error getting data!</div>
    }
  </div>;

}

export default HotelDetails
