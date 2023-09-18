import axios, { AxiosResponse, AxiosError } from 'axios'; 

import {Hotel, HotelSummary, CustomizedHotelDetails} from '../interfaces/interfaces';

export const searchHotels = (country: string, city: string, callback: ( (hs: Hotel[]) => void), errback: any) => {
  axios.post<Hotel[]>(
    'http://127.0.0.1:8000/v1/find_hotels',
    {city, country}
  )
  .then((response: AxiosResponse<Hotel[]>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}

export const baseHotelSummary = (hotel: any, requestId: string, callback: ( (hr: HotelSummary) => void), errback: any) => {
  axios.post<HotelSummary>(
    'http://127.0.0.1:8000/v1/base_hotel_summary',
    {
      request_id: requestId,
      city: hotel.city,
      country: hotel.country,
      id: hotel.id,
    }
  )
  .then((response: AxiosResponse<HotelSummary>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}

export const customizedHotelDetails = (hotelId: string, userId: string, callback: ( (cd: CustomizedHotelDetails) => void), errback: any) => {
  axios.post<CustomizedHotelDetails>(
    `http://127.0.0.1:8000/v1/customized_hotel_details/${hotelId}`,
    {user_id: userId}
  )
  .then((response: AxiosResponse<CustomizedHotelDetails>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}
