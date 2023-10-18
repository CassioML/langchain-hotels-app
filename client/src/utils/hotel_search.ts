import axios, { AxiosResponse, AxiosError } from 'axios'; 

import {Hotel, /*HotelSummary, CustomizedHotelDetails,*/ HotelReview, SuccessMarker} from '../interfaces/interfaces';
import {HotelSummaryType, CustomizedHotelDetailsType} from '../schema/data';

const base_url: string = process.env["REACT_APP_API_BASE_URL"] || "http://127.0.0.1:8000";

export const searchHotels = (country: string, city: string, callback: ( (hs: Hotel[]) => void), errback: any) => {
  axios.post<Hotel[]>(
    `${base_url}/v1/find_hotels`,
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

export const baseHotelSummary = (hotel: any, requestId: string, callback: ( (hr: HotelSummaryType) => void), errback: any) => {
  axios.post<HotelSummaryType>(
    `${base_url}/v1/base_hotel_summary`,
    {
      request_id: requestId,
      city: hotel.city,
      country: hotel.country,
      id: hotel.id,
    }
  )
  .then((response: AxiosResponse<HotelSummaryType>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}

export const customizedHotelDetails = (hotelId: string, userId: string, callback: ( (cd: CustomizedHotelDetailsType) => void), errback: any) => {
  axios.post<CustomizedHotelDetailsType>(
    `${base_url}/v1/customized_hotel_details/${hotelId}`,
    {user_id: userId}
  )
  .then((response: AxiosResponse<CustomizedHotelDetailsType>) => {
    callback(response.data);
  })
  .catch((error: AxiosError | Error) => {
    if(errback){
      errback(error);
    }
  });
}

export const addHotelReview = (hotelId: string, userId: string, review: HotelReview, callback: ((m: SuccessMarker) => void), errback: any) => {
  axios.post<SuccessMarker>(
    `${base_url}/v1/${hotelId}/add_review`,
    {
      ...review,
      ...{rating: +review.rating, id: "will-be-discarded"},  // trick to coerce into a number
    }
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