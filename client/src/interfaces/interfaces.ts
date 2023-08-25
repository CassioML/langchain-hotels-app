import { Dispatch, SetStateAction } from "react";

export interface UserDesc {
  userId: string|undefined;
}

export interface UserProps {
  userId: string|undefined;
  setUserId: Dispatch<SetStateAction<string|undefined>>;
}

export type UserProfileDesc = {
  pets: boolean;
  business: boolean;
  family_and_kids: boolean;
  sightseeing: boolean;
  fine_dining: boolean;
  adventure_and_theme_parks: boolean;
  outdoor_activities: boolean;
  clubbing_and_nightlife: boolean;
  romantic_getaway: boolean;
  relaxing: boolean;
}

export const DEFAULT_PROFILE = {
  pets: false,
  business: true,
  family_and_kids: false,
  sightseeing: true,
  fine_dining: false,
  adventure_and_theme_parks: false,
  outdoor_activities: true,
  clubbing_and_nightlife: false,
  romantic_getaway: false,
  relaxing: true,

}

// export type UserProfileDesc = {
//   userId: string;
// } & ProfileDesc;

export type RequestStatus = "initialized" | "in_flight" | "completed" | "errored"
