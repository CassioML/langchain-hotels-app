import { useState } from "react"
import {MDBInput, MDBBtn} from 'mdb-react-ui-kit';

import '../App.css';
import {LoginProps} from "../../interfaces/props";


const LoginComponent = (props: LoginProps) => {

  const {setUserId, setCurrentNavPage} = props;

  const [editUserId, setEditUserId] = useState('');

  const trySetUserId = (newUserId: string) => {
    if(newUserId){
      setUserId(newUserId);
      setCurrentNavPage("hotel_search");
    }
  }

  return (
    <form className="w-25">
      <MDBInput
        className='mb-4'
        type='text'
        id='user_id'
        label='User ID'
        value={editUserId}
        onChange={(e) => setEditUserId(e.target.value)}
        onKeyPress={(e) => {if (e.key === 'Enter') { trySetUserId(editUserId) }}}
      />
      <MDBInput className='mb-4' type='password' id='password' label='Password'
        onKeyPress={(e) => {if (e.key === 'Enter') { trySetUserId(editUserId) }}}
      />

      <MDBBtn
        type='submit'
        onClick={() => trySetUserId(editUserId)}
        block
      >
        Sign in
      </MDBBtn>
    </form>
  )
}

export default LoginComponent
