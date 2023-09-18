import axios from "axios";

export const searchHotels = (country: string, city: string, callback: any, errback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/find_hotels',
    {city, country}
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

export const baseHotelSummary = (hotel: any, requestId: string, callback: any, errback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/base_hotel_summary',
    {
      request_id: requestId,
      city: hotel.city,
      country: hotel.country,
      id: hotel.id,
    }
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

export const customizedHotelDetails = (hotelId: string, userId: string, callback: any, errback: any) => {
  axios.post(
    `http://127.0.0.1:8000/v1/customized_hotel_details/${hotelId}`,
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
