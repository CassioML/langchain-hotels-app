import axios from "axios";

import {UserProfileDesc} from "../interfaces/interfaces";

export const setAPIUserProfile = (userId: string, profileData: UserProfileDesc, callback: any, error_callback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/set_user_profile',
    {user_id: userId, profileData}
  )
  .then((response: any) => {
    callback(response.data);
  })
  .catch((error: any) => {
    if(error_callback){
      error_callback();
    }
  });
}

export const getAPIUserProfile = (userId: string, callback: any, error_callback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/get_user_profile',
    {user_id: userId}
  )
  .then((response: any) => {
    callback(response.data);
  })
  .catch((error: any) => {
    if(error_callback){
      error_callback();
    }
  });
}
