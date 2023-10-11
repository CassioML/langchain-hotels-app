import {
  MDBRow,
} from 'mdb-react-ui-kit';

import '../App.css';
import {HotelResultsProps} from "../../schema/props";
import {HotelType} from "../../schema/data";

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
        key={hotel.id}
        setSearchStep={setSearchStep}
        setDetailsHotel={setDetailsHotel}
      />) }
    </MDBRow>
  </> );
}

export default SearchResultsComponent
