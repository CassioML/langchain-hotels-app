import axios from "axios";

import {UserProfile} from "../interfaces/interfaces";

export const setAPIUserProfile = (userId: string, userProfile: UserProfile, callback: any, errback: any) => {
  const payload = {
    user_id: userId,
    user_profile: userProfile,
  };
  axios.post(
    'http://127.0.0.1:8000/v1/set_user_profile',
    payload,
  )
  .then((response: any) => {
    callback(response.data);
  })
  .catch((error: any) => {
    if(errback){
      errback();
    }
  });
}

export const getAPIUserProfile = (userId: string, callback: any, errback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/get_user_profile',
    {user_id: userId}
  )
  .then((response: any) => {
    callback(response.data);
  })
  .catch((error: any) => {
    if(errback){
      errback();
    }
  });
}
