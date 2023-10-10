import { useState } from "react"
import {MDBBreadcrumb, MDBBreadcrumbItem } from 'mdb-react-ui-kit';

import '../App.css';
import {SearchProps} from "../../schema/props";
import {HotelSearchStep} from "../../schema/enums";
import {HotelType, CustomizedHotelDetailsType} from "../../schema/data";

import SearchFormComponent from "../forms/SearchFormComponent";
import SearchResultsComponent from "../subpages/SearchResultsComponent";
import SearchDetailsComponent from "../subpages/SearchDetailsComponent";

const SearchComponent = (props: SearchProps) => {

  const {userId} = props;

  const [searchStep, setSearchStep] = useState<HotelSearchStep>("search")

  // search-stage states
  const [editHotelCountry, setEditHotelCountry] = useState('');
  const [editHotelCity, setEditHotelCity] = useState('');

  // result-stage states
  const [hotelSearchResults, setHotelSearchResults] = useState<HotelType[]>([]);

  // details-stage states
  const [detailsHotel, setDetailsHotel] = useState<HotelType>();
  const [hotelDetails, setHotelDetails] = useState<CustomizedHotelDetailsType>();

  const shortenName = (name: string) => {
    return (name.length > 24 ? name.slice(0, 24) + "..." : name);
  }

  return (<>

    { (searchStep !== "search") && <>
        <MDBBreadcrumb>
          <MDBBreadcrumbItem
            onClick={() => setSearchStep("search")}
          >
            Search
          </MDBBreadcrumbItem>
          <MDBBreadcrumbItem
            onClick={(searchStep !== "results") ? () => setSearchStep("results") : () => {}}
            active={searchStep === "results"}
          >
            Results
          </MDBBreadcrumbItem>
          { (searchStep === "details") && <>
            <MDBBreadcrumbItem active>
              {shortenName((detailsHotel || {}).name || "(unnamed hotel)")}
            </MDBBreadcrumbItem>
          </> }
        </MDBBreadcrumb>
    </> }

    { (searchStep === "search") && <SearchFormComponent
      setSearchStep={setSearchStep}
      editHotelCountry={editHotelCountry}
      setEditHotelCountry={setEditHotelCountry}
      editHotelCity={editHotelCity}
      setEditHotelCity={setEditHotelCity}
      setHotelSearchResults={setHotelSearchResults}
    /> }
    { (searchStep === "results") && <SearchResultsComponent
      hotelSearchResults={hotelSearchResults}
      setDetailsHotel={setDetailsHotel}
      setSearchStep={setSearchStep}
    /> }
    { (searchStep === "details") && <SearchDetailsComponent
      userId={userId}
      detailsHotel={detailsHotel}
      hotelDetails={hotelDetails}
      setHotelDetails={setHotelDetails}
    /> }
  </>)

}

export default SearchComponent
