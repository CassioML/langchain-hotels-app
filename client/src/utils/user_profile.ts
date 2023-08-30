import axios from "axios";

import {UserProfileBasePreferences} from "../interfaces/interfaces";

export const setAPIUserProfile = (userId: string, profileData: UserProfileBasePreferences, callback: any, error_callback: any) => {
  const payload = {
    user_id: userId,
    user_profile: {
      base_preferences: profileData,
      additional_preferences: "I love AI",
    }
  };
  axios.post(
    'http://127.0.0.1:8000/v1/set_user_profile',
    payload,
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
