import {useState} from "react"
import {MDBInput, MDBBtn, MDBRow, MDBCol, MDBSpinner, MDBTypography} from 'mdb-react-ui-kit';

import '../App.css';
import {HotelFormProps} from "../../schema/props";
import {RequestStatus} from "../../schema/enums";
import {HotelType} from "../../schema/data";

import {searchHotels} from "../../utils/hotel_search";

const SearchFormComponent = (props: HotelFormProps) => {

  const [hotelSearchStatus, setHotelSearchStatus] = useState<RequestStatus>("initialized");

  const {
    setSearchStep,
    editHotelCountry,
    setEditHotelCountry,
    editHotelCity,
    setEditHotelCity,
    setHotelSearchResults,
  } = props;

  const trySearchHotels = (country: string, city: string) => {
    if (city && country) {
      setHotelSearchStatus("in_flight")
      const callback = (results: HotelType[]) => {
        setHotelSearchResults(results);
        setSearchStep("results")
        setHotelSearchStatus("completed");
      }
      const errback = (e: any) => {
        setHotelSearchStatus("errored");
        console.log(`searchHotels ERROR: ${e}`);
      }
      searchHotels(country, city, callback, errback)
    }  
  }

  return ( <>
    { (hotelSearchStatus === "in_flight") && <>
      <MDBSpinner role='status' color='success'>
        <span className='visually-hidden'>Loading...</span>
      </MDBSpinner>
    </> }
    { (hotelSearchStatus !== "in_flight") && <>
      <form className="w-25">
        <MDBInput
          className='mb-4'
          type='text'
          id='country'
          label='Country'
          value={editHotelCountry}
          onChange={(e) => setEditHotelCountry(e.target.value.toUpperCase())}
          onKeyPress={(e) => {if (e.key === 'Enter') { trySearchHotels(editHotelCountry, editHotelCity) }}}
        />
        <MDBInput
          className='mb-4'
          type='text'
          id='city'
          label='City'
          value={editHotelCity}
          onChange={(e) => setEditHotelCity(e.target.value)}
          onKeyPress={(e) => {if (e.key === 'Enter') { trySearchHotels(editHotelCountry, editHotelCity) }}}
        />

        <MDBTypography>
          <MDBTypography tag='small'>Demo values: use "US" and any major US city ("Atlanta", "Miami" ...) Use correct capitalization.</MDBTypography>
        </MDBTypography>

        <MDBRow>
          <MDBCol>
            <MDBBtn
              type='submit'
              onClick={() => trySearchHotels(editHotelCountry, editHotelCity)}
              block
            >
              Search hotels
            </MDBBtn>
          </MDBCol>
          <MDBCol>
            <MDBBtn
              type='button'
              onClick={() => {
                setEditHotelCountry("");
                setEditHotelCity("");
                setHotelSearchStatus("initialized");
                setHotelSearchResults([]);
              }}
              block
            >
              Reset
            </MDBBtn>
          </MDBCol>
        </MDBRow>
        { (hotelSearchStatus === "errored") && <>
          <MDBRow>
            <MDBCol>
              Search errored!
            </MDBCol>
          </MDBRow>
        </> }
      </form>
    </> }
  </> )
}

export default SearchFormComponent
