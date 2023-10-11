import './App.css';
import { useEffect } from "react"
import { useForm } from "react-hook-form";

import {
  MDBInput,
  MDBCol,
  MDBRow,
  MDBBtn
} from 'mdb-react-ui-kit';


import {UserDesc, UserProfile, BASE_PREFERENCES_LABELS} from "../interfaces/interfaces";

import {setAPIUserProfile, getAPIUserProfile} from "../utils/user_profile";

const UserProfileForm = (props: UserDesc & {submitState: any, setSubmitState: any, profile: UserProfile, refreshProfile: any, autoSummary: any, setAutoSummary: any}) => {

  const {userId, submitState, setSubmitState, profile, refreshProfile, autoSummary, setAutoSummary} = props;

  const {register, handleSubmit, reset} = useForm<UserProfile>();

  const onSubmitHandler = (values: UserProfile) => {
    setSubmitState("in_flight");
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

            <MDBRow>
              <MDBCol className="preferencesTitle">
                <span>Your preferences</span>
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["adventure_and_theme_parks"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.adventure_and_theme_parks")}
                      type="checkbox"
                      id="cb_adventure_and_theme_parks"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["business"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.business")}
                      type="checkbox"
                      id="cb_business"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["clubbing_and_nightlife"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.clubbing_and_nightlife")}
                      type="checkbox"
                      id="cb_clubbing_and_nightlife"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["family_and_kids"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.family_and_kids")}
                      type="checkbox"
                      id="cb_family_and_kids"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["fine_dining"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.fine_dining")}
                      type="checkbox"
                      id="cb_fine_dining"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["outdoor_activities"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.outdoor_activities")}
                      type="checkbox"
                      id="cb_outdoor_activities"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["pets"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.pets")}
                      type="checkbox"
                      id="cb_pets"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["relaxing"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.relaxing")}
                      type="checkbox"
                      id="cb_relaxing"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["romantic_getaway"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.romantic_getaway")}
                      type="checkbox"
                      id="cb_romantic_getaway"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">{BASE_PREFERENCES_LABELS["sightseeing"]}</span>
              </MDBCol>
              <MDBCol>
                <input
                      {...register("base_preferences.sightseeing")}
                      type="checkbox"
                      id="cb_sightseeing"
                />
              </MDBCol>
            </MDBRow>

            <MDBRow>
              <MDBCol>
                <span className="preferencesLabel">More preferences ...</span>
              </MDBCol>
              <MDBCol>
                <MDBInput
                  {...register("additional_preferences")}
                  id="adpr"
                />
              </MDBCol>
            </MDBRow>

            <MDBBtn
              type='submit'
              block
              className="spacedButton"
            >
              Save
            </MDBBtn>

            <hr className="hr hr-blurry" />

            <MDBRow>
              <div className="d-flex">
                <div className="p-2">
                  Auto:
                </div>
                <div className="p-2 flex-grow-1">
                  <i>{autoSummary || "(nothing)"}</i>
                </div>
                <div className="p-2">
                  <MDBBtn
                    type='button'
                    onClick={ () => {
                      setAutoSummary("...");
                      getAPIUserProfile(
                        userId || "",
                        (api_profile: any) => {
                          setAutoSummary((api_profile || {}).travel_profile_summary || "(nothing)");
                        },
                        (e: any) => {console.log(`err ${e}`);}
                      );        
                    }}
                  >Refresh
                  </MDBBtn>
                </div>
              </div>
            </MDBRow>

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
