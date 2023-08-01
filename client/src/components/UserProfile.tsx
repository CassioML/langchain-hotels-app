import './App.css';
import {UserDesc} from "../interfaces/interfaces";

const UserProfile = (props: UserDesc) => {

  const {userId} = props;

  return (
    <div>
      USER PROFILE FOR {userId}
    </div>
  );
}

export default UserProfile
