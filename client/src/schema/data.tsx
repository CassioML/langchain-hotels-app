export interface HotelType {
  city: string;
  country: string;
  num_reviews: number;
  name: string;
  id: string;
}

export interface HotelReviewType {
  title: string;
  body: string;
  id: string;
  rating: number;
}

export interface CustomizedHotelDetailsType {
  name: string;
  reviews: HotelReviewType[];
  summary: string;
}