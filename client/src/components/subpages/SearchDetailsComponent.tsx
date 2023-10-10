import { useState, useEffect } from "react"
import {
  MDBCard,
  MDBCardTitle,
  MDBCardText,
  MDBCardBody,
  MDBCardHeader,
  MDBSpinner,
  MDBCol,
  MDBRow,
  MDBBtn,
} from 'mdb-react-ui-kit';

import '../App.css';
import {HotelDetailsProps} from "../../schema/props";
import {RequestStatus} from "../../schema/enums";
import {HotelReviewType} from "../../schema/data";

import {customizedHotelDetails} from "../../utils/hotel_search";

const SearchDetailsComponent = (props: HotelDetailsProps) => {

  const {
    userId,
    detailsHotel,
    hotelDetails,
    setHotelDetails,
  } = props;

  const [detailsStatus, setDetailsStatus] = useState<RequestStatus>("initialized");

  useEffect(
    () => {
      console.log(`asking for customized details on ${(detailsHotel || {}).id} for ${userId}`);
      setDetailsStatus("in_flight")

      const callback = (results: any) => {
        setHotelDetails(results);
        setDetailsStatus("completed");
      }

      const errback = () => {
        setDetailsStatus("errored");
        console.log("ERROR (customizedHotelDetails)!");
      }

      customizedHotelDetails((detailsHotel || {}).id || "", userId || "", callback, errback);
    },
    [detailsHotel, userId]
  );

  return ( <>
    { (detailsStatus === "in_flight") && <>
      <MDBSpinner role='status' color='success'>
        <span className='visually-hidden'>Loading...</span>
      </MDBSpinner>
    </> }
    { (detailsStatus === "errored") && <>
      <MDBRow>
        <MDBCol>
          Could not get hotel customized details.
        </MDBCol>
      </MDBRow>
    </> }
    { (detailsStatus !== "in_flight" && detailsStatus !== "errored") && <>
      <MDBCard background='secondary' className='text-white mb-3'>
        <MDBCardHeader>For you</MDBCardHeader>
        <MDBCardBody>
          <MDBCardTitle>Your personal summary for "{(detailsHotel || {}).name || "(no hotel name)"}"</MDBCardTitle>
          <MDBCardText>
            {(hotelDetails || {}).summary || "(no personal summary)"}
          </MDBCardText>
        </MDBCardBody>
      </MDBCard>
      <hr className="hr hr-blurry" />
      <h3>
        Reviews chosen for you:
        <MDBBtn className="inlineButton">
          Post a review...
        </MDBBtn>        
      </h3>
      { ((hotelDetails || {}).reviews || []).map( (r: HotelReviewType) =>
        <MDBCard shadow='0' border='info' background='white' className='mb-3'>
          <MDBCardHeader>Rating: {r.rating}</MDBCardHeader>
          <MDBCardBody>
            <MDBCardTitle>{r.title}</MDBCardTitle>
            <MDBCardText>{r.body}</MDBCardText>
          </MDBCardBody>
        </MDBCard>
      ) }
    </> }
  </> );
}

export default SearchDetailsComponent
