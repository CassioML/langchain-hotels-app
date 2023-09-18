import { Dispatch, SetStateAction } from "react";

export interface UserDesc {
  userId: string|undefined;
}

export interface UserProps {
  userId: string|undefined;
  setUserId: Dispatch<SetStateAction<string|undefined>>;
}

export type UserProfileBasePreferences = {
  adventure_and_theme_parks: boolean;
  business: boolean;
  clubbing_and_nightlife: boolean;
  family_and_kids: boolean;
  fine_dining: boolean;
  outdoor_activities: boolean;
  pets: boolean;
  relaxing: boolean;
  romantic_getaway: boolean;
  sightseeing: boolean;
}

const DEFAULT_BASE_PREFERENCES = {
  adventure_and_theme_parks: false,
  business: true,
  clubbing_and_nightlife: true,
  family_and_kids: true,
  fine_dining: true,
  outdoor_activities: true,
  pets: true,
  relaxing: true,
  romantic_getaway: true,
  sightseeing: true,
}

export const BASE_PREFERENCES_LABELS = {
  adventure_and_theme_parks: "Enjoys adventure and theme parks",
  business: "Travels for business",
  clubbing_and_nightlife: "Enjoys clubbing and nightlife",
  family_and_kids: "Travels with family",
  fine_dining: "Enjoys fine dining and gourmet restaurants",
  outdoor_activities: "Loves outdoor activities",
  pets: "Cares about pets",
  relaxing: "Enjoys a relaxing holiday",
  romantic_getaway: "Travels for a romantic getaway",
  sightseeing: "Loves sightseeing",
}

export type UserProfile = {
  base_preferences: UserProfileBasePreferences;
  additional_preferences: string;
}

export const DEFAULT_USER_PROFILE = {
  base_preferences: DEFAULT_BASE_PREFERENCES,
  additional_preferences: "",
}
