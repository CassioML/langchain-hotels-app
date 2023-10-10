import { useState, useEffect } from "react"
import {
  MDBCard,
  MDBCardImage,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardFooter,
  // MDBRow,
  MDBCol,
  MDBBtn
} from 'mdb-react-ui-kit';

import '../App.css';
import {HotelCardProps} from "../../schema/props";
import {RequestStatus} from "../../schema/enums";
import {HotelType} from "../../schema/data";

import {baseHotelSummary} from "../../utils/hotel_search";

const HotelCardComponent = (props: HotelCardProps) => {

  const [summaryStatus, setSummaryStatus] = useState<RequestStatus>("initialized");
  const [hotelSummary, setHotelSummary] = useState<string | undefined>(undefined);

  const {
    hotel,
    setDetailsHotel,
    setSearchStep,
  } = props;

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

  const rndHotelIndex = (hotel: HotelType) => {
    return 1 + (hotel.id.charCodeAt(0) + hotel.id.charCodeAt(1) + hotel.id.charCodeAt(7)) % 100;
  }

  return ( <MDBCol>
    <MDBCard className='h-100'>
      <MDBCardBody>
        <MDBCardImage
          className="hotelThumbnail"
          src={`https://source.unsplash.com/collection/2048188/${rndHotelIndex(hotel)}`}
          position='top'
        />
        <MDBCardTitle>{hotel.name}</MDBCardTitle>
        <MDBCardText>
          { (summaryStatus === "in_flight") && <span>
            ...
          </span> }
          { (summaryStatus === "errored") && <span>
            (Could not get hotel summary)
          </span> }
          { (summaryStatus !== "in_flight" && summaryStatus !== "errored") && <span>
            {hotelSummary || "(no summary available)"}
          </span> }
        </MDBCardText>
        <MDBBtn
          onClick={() => {setDetailsHotel(hotel); setSearchStep("details");}}
        >
          Details
        </MDBBtn>
      </MDBCardBody>
      <MDBCardFooter>
        <small className='text-muted'>{hotel.city}, {hotel.country} / {hotel.num_reviews} review{(hotel.num_reviews !== 1) ? "s" : ""}</small>
      </MDBCardFooter>
    </MDBCard>
  </MDBCol> );
}

export default HotelCardComponent
