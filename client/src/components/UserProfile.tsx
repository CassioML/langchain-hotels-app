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
          sightseeing: api_profile.sightseeing,
          business: api_profile.business,
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
