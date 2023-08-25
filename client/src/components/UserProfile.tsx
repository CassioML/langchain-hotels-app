import './App.css';

import { useEffect, useState } from "react"

import {UserDesc, UserProfileDesc, RequestStatus, DEFAULT_PROFILE} from "../interfaces/interfaces";
import {getAPIUserProfile} from "../utils/user_profile";

import UserProfileForm from "./UserProfileForm"

const UserProfile = (props: UserDesc) => {

  const {userId} = props;

  const [submitState, setSubmitState] = useState<RequestStatus>("initialized");
  const [profile, setProfile] = useState<UserProfileDesc>(DEFAULT_PROFILE);

  const refreshProfile = () => {
    setSubmitState("in_flight");
    getAPIUserProfile(
      userId || "",
      (api_profile: any) => {
        const this_profile: UserProfileDesc = {
          pets: api_profile.pets,
          business: api_profile.business,
          family_and_kids: api_profile.family_and_kids,
          sightseeing: api_profile.sightseeing,
          fine_dining: api_profile.fine_dining,
          adventure_and_theme_parks: api_profile.adventure_and_theme_parks,
          outdoor_activities: api_profile.outdoor_activities,
          clubbing_and_nightlife: api_profile.clubbing_and_nightlife,
          romantic_getaway: api_profile.romantic_getaway,
          relaxing: api_profile.relaxing,

        };
        setProfile(this_profile);
        setSubmitState("completed");
      },
      (e: any) => {console.log(`err ${e}`); setSubmitState("errored");}
    );
  }

  useEffect(
    refreshProfile,
    [userId]
  );


  return (
    <div>
      USER PROFILE FOR {userId}
      <UserProfileForm
        userId={userId}
        submitState={submitState}
        setSubmitState={setSubmitState}
        profile={profile}
        refreshProfile={refreshProfile}
      />
    </div>
  );
}

export default UserProfile
