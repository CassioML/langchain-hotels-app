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
  sightseeing: boolean;  
}

export const DEFAULT_PROFILE = {
  pets: false,
  business: true,
  sightseeing: false,
}

// export type UserProfileDesc = {
//   userId: string;
// } & ProfileDesc;

export type RequestStatus = "initialized" | "in_flight" | "completed" | "errored"
