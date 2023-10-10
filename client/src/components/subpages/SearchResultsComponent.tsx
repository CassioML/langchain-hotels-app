// import { useState } from "react"
import {
  // MDBCard,
  // MDBCardImage,
  // MDBCardBody,
  // MDBCardTitle,
  // MDBCardText,
  // MDBCardFooter,
  MDBRow,
  // MDBCol,
  // MDBBtn
} from 'mdb-react-ui-kit';

import '../App.css';
import {HotelResultsProps} from "../../schema/props";
// import {RequestStatus} from "../../schema/enums";
import {HotelType} from "../../schema/data";

import {baseHotelSummary} from "../../utils/hotel_search";

import HotelCardComponent from "../cards/HotelCardComponent";

const SearchResultsComponent = (props: HotelResultsProps) => {


  const {
    hotelSearchResults,
    setSearchStep,
    setDetailsHotel,
  } = props;

  return ( <>
    <MDBRow className='row-cols-1 row-cols-md-3 g-4'>
      { hotelSearchResults.map( (hotel: HotelType) => <HotelCardComponent
        hotel={hotel}
        setSearchStep={setSearchStep}
        setDetailsHotel={setDetailsHotel}
      />) }
    </MDBRow>
  </> );
}

export default SearchResultsComponent
