import './App.css';
// import { useEffect } from "react"
import { useForm } from "react-hook-form";

import {HotelReview} from "../interfaces/interfaces";
import {addHotelReview} from "../utils/hotel_search";

const AddReviewForm = (props: {userId: string, hotelId: string, submitState: any, setSubmitState: any}) => {

  const {userId, hotelId, submitState, setSubmitState} = props;

  const {register, handleSubmit, reset} = useForm<HotelReview>();

  const onSubmitHandler = (values: HotelReview) => {
    // console.log(`REV ${JSON.stringify(values)}`);
    setSubmitState("in_flight");
    addHotelReview(
      hotelId,
      userId || "",
      values,
      (response: any) => {
        if (response.success){
          reset();
          setSubmitState("completed");
        }else{
          console.log(`success was false`);
          setSubmitState("errored");
        }
      },
      (e: any) => {console.log(`err setting: ${e}`); setSubmitState("errored");}
    );
  };

  // useEffect(
  //   () => {reset(profile);},
  //   [profile, reset]
  // );

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
            <label htmlFor="r_title">Title</label>
            <input
                  {...register("title")}
                  id="r_title"
            />

            <label htmlFor="r_body">Body</label>
            <input
                  {...register("body")}
                  id="r_body"
            />

            <label htmlFor="r_rating">Rating</label>
            <input
                  {...register("rating")}
                  id="r_rating"
            />
            <button type="submit" className="inlineButton">Post</button>
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

export default AddReviewForm
