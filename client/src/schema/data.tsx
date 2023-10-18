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
  summary: string[];
}

export interface SuccessMarkerType {
  success: boolean;
}

export interface HotelSummaryType {
  request_id: string;
  reviews: HotelReviewType[];
  summary: string[];
}
