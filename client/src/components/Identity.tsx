import { /*useEffect,*/ useState } from "react"

import {UserProps} from "../interfaces/interfaces";
import './App.css';


const Identity = (props: UserProps & {setCurrentUserPage: any}) => {

  const userId = props.userId;
  const setUserId = props.setUserId;
  const setCurrentUserPage = props.setCurrentUserPage;

  const [editUserId, setEditUserId] = useState('');

  const trySetUserId = (newUserId: string) => {
    if(newUserId){
      setUserId(newUserId);
      setCurrentUserPage("hotel_search");
    }
  }

  return (
    <div className="App-identity">
      { !userId && <div>
        <p>
          Who are you?
          <input
            className="inlineInput"
            type="text"
            name="userid"
            value={editUserId}
            onChange={(e) => setEditUserId(e.target.value)}
            onKeyPress={(e) => {if (e.key === 'Enter') { trySetUserId(editUserId) }}}
          />
          <button
            onClick={() => trySetUserId(editUserId)}
            className="inlineButton"
          >
            Login
          </button>
        </p>
      </div>}
      { userId && <div>
        <p>
          Welcome, <span className="userName">{userId}</span>

          <button
            onClick={() => {
              setUserId(undefined);
            }}
            className="inlineButton"
          >
            Logout
          </button>

        </p>

      </div>}
    </div>
  );
}

export default Identity
