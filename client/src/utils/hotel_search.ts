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
