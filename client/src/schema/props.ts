import { Dispatch, SetStateAction } from "react";

import {NavPage, HotelSearchStep} from "./enums";
import {HotelType, CustomizedHotelDetailsType} from "./data";

export interface LoginProps {
  setUserId: Dispatch<SetStateAction<string|undefined>>;
  setCurrentNavPage: Dispatch<SetStateAction<NavPage>>;
}

export interface PreferencesProps {
  userId: string|undefined;
}

export interface SearchProps {
  userId: string|undefined;
}

export interface HotelFormProps {
  setSearchStep: Dispatch<SetStateAction<HotelSearchStep>>;
  editHotelCountry: string;
  setEditHotelCountry: Dispatch<SetStateAction<string>>;
  editHotelCity: string;
  setEditHotelCity: Dispatch<SetStateAction<string>>;
  setHotelSearchResults: Dispatch<SetStateAction<HotelType[]>>
}

export interface HotelResultsProps {
  hotelSearchResults: HotelType[];
  setDetailsHotel: Dispatch<SetStateAction<HotelType|undefined>>;
  setSearchStep: Dispatch<SetStateAction<HotelSearchStep>>;
}

export interface HotelCardProps {
  hotel: HotelType;
  setDetailsHotel: Dispatch<SetStateAction<HotelType|undefined>>;
  setSearchStep: Dispatch<SetStateAction<HotelSearchStep>>;
}

export interface HotelDetailsProps {
  userId: string|undefined;
  detailsHotel: HotelType | undefined;
  hotelDetails: CustomizedHotelDetailsType|undefined;
  setHotelDetails: Dispatch<SetStateAction<CustomizedHotelDetailsType|undefined>>;
  setSearchStep: Dispatch<SetStateAction<HotelSearchStep>>;
}

export interface PostHotelReviewFormProps {
  userId: string|undefined;
  detailsHotel: HotelType | undefined;
  setSearchStep: Dispatch<SetStateAction<HotelSearchStep>>;
  editReviewTitle: string;
  setEditReviewTitle: Dispatch<SetStateAction<string>>;
  editReviewBody: string;
  setEditReviewBody: Dispatch<SetStateAction<string>>;
  editReviewRating: string;
  setEditReviewRating: Dispatch<SetStateAction<string>>;
}
