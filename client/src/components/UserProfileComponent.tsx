import './App.css';

import { useEffect, useState } from "react"

import {UserDesc, UserProfile, UserProfileBasePreferences, DEFAULT_USER_PROFILE} from "../interfaces/interfaces";
import {RequestStatus} from "../interfaces/enums";
import {getAPIUserProfile} from "../utils/user_profile";

import UserProfileForm from "./UserProfileForm"

const UserProfileComponent = (props: UserDesc) => {

  const {userId} = props;

  const [submitState, setSubmitState] = useState<RequestStatus>("initialized");
  const [profile, setProfile] = useState<UserProfile>(DEFAULT_USER_PROFILE);

  const refreshProfile = () => {
    setSubmitState("in_flight");
    getAPIUserProfile(
      userId || "",
      (api_profile: any) => {
        const _profile = api_profile || {};
        const base_preferences = _profile.base_preferences || {};
        const these_base_prefs: UserProfileBasePreferences = {
          ...DEFAULT_USER_PROFILE.base_preferences,
          ...base_preferences,
        }
        const this_profile = {
          base_preferences: these_base_prefs,
          additional_preferences: _profile.additional_preferences,
        }
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

export default UserProfileComponent
