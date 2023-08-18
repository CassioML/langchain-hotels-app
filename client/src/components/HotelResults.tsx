import './App.css';

// import {RequestStatus} from "../interfaces/interfaces";

const HotelResults = (props: any) => {

  const {searchStatus, searchResults} = props;

  if (searchStatus === "initialized") {
    return <div></div>;
  } else if (searchStatus === "in_flight") {
    return <div>Searching ...</div>;
  } else if (searchStatus === "completed") {
    return <div>
      <ul>
        {searchResults.map( (r: any) => <li key={r.id}>{`${r.name} (${r.id})`}</li>)}
      </ul>
    </div>
  } else {
    return <div>Search errored!</div>;
  }
}

export default HotelResults
