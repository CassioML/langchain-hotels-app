import axios from "axios";

export const searchHotels = (country: string, city: string, callback: any, error_callback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/find_hotels',
    {city, country}
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

export const baseHotelSummary = (hotel: any, request_id: string, callback: any, error_callback: any) => {
  axios.post(
    'http://127.0.0.1:8000/v1/base_hotel_summary',
    {
      request_id: request_id,
      city: hotel.city,
      country: hotel.country,
      id: hotel.id,
    }
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

export const customizedHotelDetails = (hotel_id: string, callback: any, error_callback: any) => {
  axios.post(
    `http://127.0.0.1:8000/v1/customized_hotel_details/${hotel_id}`,
    {}
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
