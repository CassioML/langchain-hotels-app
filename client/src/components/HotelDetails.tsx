import './App.css';

import { useEffect, useState } from "react";

import { useParams } from "react-router-dom";

import {customizedHotelDetails} from "../utils/hotel_search";
import {RequestStatus} from "../interfaces/interfaces";

const HotelDetails = (props: any) => {

  const {hotel_id} = useParams();

  const [hotelDetails, setHotelDetails] = useState<any>();
  const [detailsStatus, setDetailsStatus] = useState<RequestStatus>("initialized");

  useEffect(
    () => {
      console.log(`asking for customized details on ${hotel_id}`);
      setDetailsStatus("in_flight")

      const callback = (results: any) => {
        setHotelDetails(results);
        setDetailsStatus("completed");
      }

      const err_back = () => {
        setDetailsStatus("errored");
        console.log("ERROR (baseHotelSummary)!");
      }

      customizedHotelDetails(hotel_id || "", callback, err_back);
    },
    [hotel_id]
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
