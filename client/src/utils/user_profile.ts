import axios, { AxiosResponse, AxiosError } from 'axios'; 

import {UserProfile, SuccessMarker} from "../interfaces/interfaces";

export const setAPIUserProfile = (userId: string, userProfile: UserProfile, callback: ((m: SuccessMarker) => void), errback: any) => {
  const payload = {
    user_id: userId,
    user_profile: userProfile,
  };
  axios.post<SuccessMarker>(
    'http://127.0.0.1:8000/v1/set_user_profile',
    payload,
  )
  .then((response: AxiosResponse<SuccessMarker>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}

export const getAPIUserProfile = (userId: string, callback: (( p: UserProfile | undefined ) => void), errback: any) => {
  axios.post<UserProfile | undefined>(
    'http://127.0.0.1:8000/v1/get_user_profile',
    {user_id: userId}
  )
  .then((response: AxiosResponse<UserProfile | undefined>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}
