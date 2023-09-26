// import React from 'react';
import { /*useEffect,*/ useState } from "react"

import './App.css';

import Identity from './Identity';
import SiteContents from './SiteContents';

import {UserPage} from "../interfaces/enums";

function App() {

  const [userId, setUserId] = useState<string>();
  const [currentUserPage, setCurrentUserPage] = useState<UserPage>("hotel_search");

  return (
    <div className="App">
      <header className="App-header">
        <p>Hotel finder</p>
      </header>
      <div className="App-body">
        <Identity
          userId={userId}
          setUserId={setUserId}
          setCurrentUserPage={setCurrentUserPage}
        />
        <hr />
        <SiteContents
          userId={userId}
          currentUserPage={currentUserPage}
          setCurrentUserPage={setCurrentUserPage}
        />
      </div>
    </div>
  );
}

export default App;
