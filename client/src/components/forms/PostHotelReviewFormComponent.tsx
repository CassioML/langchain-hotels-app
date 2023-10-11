import {useState} from "react"
import {MDBInput, MDBBtn, MDBRow, MDBCol, MDBSpinner, MDBTypography} from 'mdb-react-ui-kit';

import '../App.css';
import {PostHotelReviewFormProps} from "../../schema/props";
import {RequestStatus} from "../../schema/enums";
import {HotelType, HotelReviewType, SuccessMarkerType} from "../../schema/data";

import {addHotelReview} from "../../utils/hotel_search";

const PostHotelReviewFormComponent = (props: PostHotelReviewFormProps) => {

  const [hotelReviewPostStatus, setHotelReviewPostStatus] = useState<RequestStatus>("initialized");
  const [reviewPosted, setReviewPosted] = useState(false);

  const {
    userId,
    detailsHotel,
    setSearchStep,
    editReviewTitle,
    setEditReviewTitle,
    editReviewBody,
    setEditReviewBody,
    editReviewRating,
    setEditReviewRating,
  } = props;

  const tryAddHotelReview = (userId: string|undefined, hotel: HotelType|undefined, title: string, body: string, rating_str: string) => {
    if (userId && hotel && title && body && rating_str && !isNaN(+rating_str)) {
      const rating = +rating_str
      setHotelReviewPostStatus("in_flight")
      const callback = (success: SuccessMarkerType) => {
        setEditReviewTitle("");
        setEditReviewBody("");
        setEditReviewRating("");
        setHotelReviewPostStatus("completed");
        setReviewPosted(true);
      }
      const errback = (e: any) => {
        setHotelReviewPostStatus("errored");
        console.log(`tryAddHotelReview ERROR: ${e}`);
      }
      const newReview: HotelReviewType = {
        title: title,
        body: body,
        id: "discarded",
        rating: rating,
      };
      addHotelReview(hotel.id, userId, newReview, callback, errback)
    }  
  }

  return ( <>
    { reviewPosted && <>
      <MDBRow>
        <MDBCol>
          <MDBTypography note noteColor='secondary'>
            <strong>Thank you for posting your review.</strong> You can now go back to "{(detailsHotel || {}).name || "(unnamed hotel)"}".
            <MDBBtn size="sm" className="inlineButton" onClick={ () => setSearchStep("details")}>Back</MDBBtn>
          </MDBTypography>
        </MDBCol>
      </MDBRow>
    </> }
    { (!reviewPosted) && <>
      { (hotelReviewPostStatus === "in_flight") && <>
        <MDBSpinner role='status' color='success'>
          <span className='visually-hidden'>Loading...</span>
        </MDBSpinner>
      </> }
      { (hotelReviewPostStatus !== "in_flight") && <>
        <form className="w-25">
          <MDBInput
            className='mb-4'
            type='text'
            id='title'
            label='Title'
            value={editReviewTitle}
            onChange={(e) => setEditReviewTitle(e.target.value)}
            onKeyPress={(e) => {if (e.key === 'Enter') { tryAddHotelReview(userId, detailsHotel, editReviewTitle, editReviewBody, editReviewRating) }}}
          />
          <MDBInput
            className='mb-4'
            type='text'
            id='body'
            label='Body'
            value={editReviewBody}
            onChange={(e) => setEditReviewBody(e.target.value)}
            onKeyPress={(e) => {if (e.key === 'Enter') { tryAddHotelReview(userId, detailsHotel, editReviewTitle, editReviewBody, editReviewRating) }}}
          />
          <MDBInput
            className='mb-4'
            type='text'
            id='rating'
            label='Rating 0-10'
            value={editReviewRating}
            onChange={(e) => setEditReviewRating(e.target.value)}
            onKeyPress={(e) => {if (e.key === 'Enter') { tryAddHotelReview(userId, detailsHotel, editReviewTitle, editReviewBody, editReviewRating) }}}
          />

          <MDBRow>
            <MDBCol>
              <MDBBtn
                type='button'
                onClick={() => tryAddHotelReview(userId, detailsHotel, editReviewTitle, editReviewBody, editReviewRating)}
                block
              >
                Post
              </MDBBtn>
            </MDBCol>
            <MDBCol>
              <MDBBtn
                type='button'
                onClick={() => {
                  setEditReviewTitle("");
                  setEditReviewBody("");
                  setEditReviewRating("");
                  setHotelReviewPostStatus("initialized");
                }}
                block
              >
                Reset
              </MDBBtn>
            </MDBCol>
          </MDBRow>
          { (hotelReviewPostStatus === "errored") && <>
            <MDBRow>
              <MDBCol>
                Post errored!
              </MDBCol>
            </MDBRow>
          </> }
        </form>
      </> }
    </> }
  </> )
}

export default PostHotelReviewFormComponent
