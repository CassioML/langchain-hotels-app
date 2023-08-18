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
                <label htmlFor="pets">Cares about pets</label>
                <input {...register("pets")} name="pets" id="pets" type="checkbox" />
              </li>
            
              <li>
                <label htmlFor="business">Travel for business</label>
                <input {...register("business")} name="business" id="business" type="checkbox" />
              </li>
            
              <li>
                <label htmlFor="sightseeing">Loves sightseeing</label>
                <input {...register("sightseeing")} name="sightseeing" id="sightseeing" type="checkbox" />
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
