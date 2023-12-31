import {useState, useEffect} from "react"
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
  MDBTypography,
  MDBIcon,
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
    setSearchStep,
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
    [detailsHotel, setHotelDetails, userId]
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
            <MDBTypography listUnStyled className='mb-0'>
              { ((hotelDetails || {}).summary || ["(no personal summary)"]).map( (itm, i) =>
                  <li key={i} className='mb-1'>
                    <MDBIcon fas icon="sticky-note" className='me-2 text-warning' />
                    {itm}
                  </li>
                )
              }
            </MDBTypography>
          </MDBCardText>
        </MDBCardBody>
      </MDBCard>
      <hr className="hr hr-blurry" />
      <h3>
        Reviews chosen for you:
        <MDBBtn
          className="inlineButton"
          onClick={() => setSearchStep("post_review")}
        >
          Post a review...
        </MDBBtn>        
      </h3>
      { ((hotelDetails || {}).reviews || []).map( (r: HotelReviewType) =>
        <MDBCard shadow='0' border='info' background='white' className='mb-3' key={r.id}>
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
