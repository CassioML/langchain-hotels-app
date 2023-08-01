import './App.css';

const HotelResults = (props: any) => {

  const {searchStatus, searchResults} = props;

  if (searchStatus === 0) {
    return <div></div>;
  } else if (searchStatus === 1) {
    return <div>Searching ...</div>;
  } else {
    // assume results are there
    console.log(JSON.stringify(searchResults));
    return <div>
      <ul>
        {searchResults.map( (r: any) => <li id={r.id}>{`${r.name} (${r.id})`}</li>)}
      </ul>
    </div>
  }
}

export default HotelResults
