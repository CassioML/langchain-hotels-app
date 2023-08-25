import './App.css';
import { useEffect } from "react"
import { useForm } from "react-hook-form";

import {UserDesc, UserProfileDesc} from "../interfaces/interfaces";

import {setAPIUserProfile} from "../utils/user_profile";

const UserProfileForm = (props: UserDesc & {submitState: any, setSubmitState: any, profile: UserProfileDesc, refreshProfile: any}) => {

  const {userId, submitState, setSubmitState, profile, refreshProfile} = props;

  const {register, handleSubmit, reset} = useForm<UserProfileDesc>();

  const onSubmitHandler = (values: UserProfileDesc) => {
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
            <ul>
            
              <li>
                <label htmlFor="business">Travels for business</label>
                <input {...register("business")} name="business" id="business" type="checkbox" />
              </li>

              <li>
                <label htmlFor="family_and_kids">Travels with family</label>
                <input {...register("family_and_kids")} name="family_and_kids" id="family_and_kids" type="checkbox" />
              </li>
              
              <li>
                <label htmlFor="romantic_getaway">Travels for a romantic getaway</label>
                <input {...register("romantic_getaway")} name="romantic_getaway" id="romantic_getaway" type="checkbox" />
              </li>
            
              <li>
                <label htmlFor="sightseeing">Loves sightseeing</label>
                <input {...register("sightseeing")} name="sightseeing" id="sightseeing" type="checkbox" />
              </li>

              <li>
                <label htmlFor="fine_dining">Enjoys fine dining and gourmet restaurants</label>
                <input {...register("fine_dining")} name="fine_dining" id="fine_dining" type="checkbox" />
              </li>

              <li>
                <label htmlFor="adventure_and_theme_parks">Enjoys adventure and theme parks</label>
                <input {...register("adventure_and_theme_parks")} name="adventure_and_theme_parks" id="adventure_and_theme_parks" type="checkbox" />
              </li>

              <li>
                <label htmlFor="outdoor_activities">Loves outdoor activities</label>
                <input {...register("outdoor_activities")} name="outdoor_activities" id="outdoor_activities" type="checkbox" />
              </li>

              <li>
                <label htmlFor="clubbing_and_nightlife">Enjoys clubbing and nightlife</label>
                <input {...register("clubbing_and_nightlife")} name="clubbing_and_nightlife" id="clubbing_and_nightlife" type="checkbox" />
              </li>

              <li>
                <label htmlFor="relaxing">Enjoys a relaxing holiday</label>
                <input {...register("relaxing")} name="relaxing" id="relaxing" type="checkbox" />
              </li>

              <li>
                <label htmlFor="pets">Cares about pets</label>
                <input {...register("pets")} name="pets" id="pets" type="checkbox" />
              </li>

            </ul>
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
