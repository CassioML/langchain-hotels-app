import './App.css';

import { useEffect, useState } from "react"

import {UserDesc, UserProfileBasePreferences, RequestStatus, DEFAULT_BASE_PREFERENCES} from "../interfaces/interfaces";
import {getAPIUserProfile} from "../utils/user_profile";

import UserProfileForm from "./UserProfileForm"

const UserProfile = (props: UserDesc) => {

  const {userId} = props;

  const [submitState, setSubmitState] = useState<RequestStatus>("initialized");
  const [profile, setProfile] = useState<UserProfileBasePreferences>(DEFAULT_BASE_PREFERENCES);

  const refreshProfile = () => {
    setSubmitState("in_flight");
    getAPIUserProfile(
      userId || "",
      (api_profile: any) => {
        const _profile = api_profile || {};
        const base_preferences = api_profile.base_preferences || {};
        const these_base_prefs: UserProfileBasePreferences = {
          ...DEFAULT_BASE_PREFERENCES,
          ...base_preferences,
        }
        setProfile(these_base_prefs);
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
