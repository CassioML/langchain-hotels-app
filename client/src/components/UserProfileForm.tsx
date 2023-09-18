import './App.css';
import { useEffect } from "react"
import { useForm } from "react-hook-form";

import {UserDesc, UserProfile, BASE_PREFERENCES_LABELS} from "../interfaces/interfaces";

import {setAPIUserProfile} from "../utils/user_profile";

const UserProfileForm = (props: UserDesc & {submitState: any, setSubmitState: any, profile: UserProfile, refreshProfile: any}) => {

  const {userId, submitState, setSubmitState, profile, refreshProfile} = props;

  const {register, handleSubmit, reset} = useForm<UserProfile>();

  const onSubmitHandler = (values: UserProfile) => {
    setSubmitState("in_flight");
    // console.log(`values = ${JSON.stringify(values)}`);
    setAPIUserProfile(
      userId || "",
      values,
      (response: any) => {
        if (response.success){
          refreshProfile();
        }else{
          console.log(`success was false`);
          setSubmitState("errored");
        }
      },
      (e: any) => {console.log(`err setting: ${e}`); setSubmitState("errored");}
    );
  };

  useEffect(
    () => {reset(profile);},
    [profile, reset]
  );

  if (submitState === "initialized" || submitState === "errored" || submitState === "completed"){
    return (
      <div>
        { (submitState === "errored") && 
          <div>
            Submission errored!
          </div>
        }
        <form onSubmit={handleSubmit(onSubmitHandler)} className="form">
          <div>
            <ul>

              <li>
                <input
                      {...register("base_preferences.adventure_and_theme_parks")}
                      type="checkbox"
                      id="cb_adventure_and_theme_parks"
                />
                <label htmlFor="cb_adventure_and_theme_parks">{BASE_PREFERENCES_LABELS["adventure_and_theme_parks"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.business")}
                      type="checkbox"
                      id="cb_business"
                />
                <label htmlFor="cb_business">{BASE_PREFERENCES_LABELS["business"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.clubbing_and_nightlife")}
                      type="checkbox"
                      id="cb_clubbing_and_nightlife"
                />
                <label htmlFor="cb_clubbing_and_nightlife">{BASE_PREFERENCES_LABELS["clubbing_and_nightlife"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.family_and_kids")}
                      type="checkbox"
                      id="cb_family_and_kids"
                />
                <label htmlFor="cb_family_and_kids">{BASE_PREFERENCES_LABELS["family_and_kids"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.fine_dining")}
                      type="checkbox"
                      id="cb_fine_dining"
                />
                <label htmlFor="cb_fine_dining">{BASE_PREFERENCES_LABELS["fine_dining"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.outdoor_activities")}
                      type="checkbox"
                      id="cb_outdoor_activities"
                />
                <label htmlFor="cb_outdoor_activities">{BASE_PREFERENCES_LABELS["outdoor_activities"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.pets")}
                      type="checkbox"
                      id="cb_pets"
                />
                <label htmlFor="cb_pets">{BASE_PREFERENCES_LABELS["pets"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.relaxing")}
                      type="checkbox"
                      id="cb_relaxing"
                />
                <label htmlFor="cb_relaxing">{BASE_PREFERENCES_LABELS["relaxing"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.romantic_getaway")}
                      type="checkbox"
                      id="cb_romantic_getaway"
                />
                <label htmlFor="cb_romantic_getaway">{BASE_PREFERENCES_LABELS["romantic_getaway"]}</label>
              </li>

              <li>
                <input
                      {...register("base_preferences.sightseeing")}
                      type="checkbox"
                      id="cb_sightseeing"
                />
                <label htmlFor="cb_sightseeing">{BASE_PREFERENCES_LABELS["sightseeing"]}</label>
              </li>

            </ul>
            <p>
              <label htmlFor="adpr">Add Pref</label>
              <input
                    {...register("additional_preferences")}
                    id="adpr"
              />
            </p>
            <button type="submit" className="inlineButton">Save</button>
          </div>
        </form>
      </div>
    );
  } else if (submitState === "in_flight"){
    return <p>Please wait ...</p>
  } else {
    return <p>(trouble with form) {submitState}</p>
  }
}

export default UserProfileForm
