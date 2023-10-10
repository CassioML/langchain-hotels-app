import { useEffect, useState } from "react"
import { MDBCol } from 'mdb-react-ui-kit';

import '../App.css';

import {UserDesc, UserProfile, UserProfileBasePreferences, DEFAULT_USER_PROFILE} from "../../interfaces/interfaces"; // TODO
import {RequestStatus} from "../../schema/enums";
import {PreferencesProps} from "../../schema/props";

import {getAPIUserProfile} from "../../utils/user_profile";

import UserProfileForm from "../UserProfileForm";

const PreferencesComponent = (props: PreferencesProps) => {

  const {userId} = props;

  const [submitState, setSubmitState] = useState<RequestStatus>("initialized");
  const [profile, setProfile] = useState<UserProfile>(DEFAULT_USER_PROFILE);

  const [autoSummary, setAutoSummary] = useState<string | undefined>();

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
          travel_profile_summary: _profile.travel_profile_summary,
        }
        setProfile(this_profile);
        setAutoSummary(this_profile.travel_profile_summary);
        setSubmitState("completed");
      },
      (e: any) => {console.log(`err ${e}`); setSubmitState("errored");}
    );
  }

  useEffect(
    refreshProfile,
    [userId]
  );


  return ( <>
    <div className="d-flex flex-column mb-3 col-md-6">
      <UserProfileForm
        userId={userId}
        submitState={submitState}
        setSubmitState={setSubmitState}
        profile={profile}
        refreshProfile={refreshProfile}
        autoSummary={autoSummary}
        setAutoSummary={setAutoSummary}
      />
    </div>
  </> );

}

export default PreferencesComponent
