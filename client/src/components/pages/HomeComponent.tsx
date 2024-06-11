import { useState } from "react"

import {
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardImage,
  MDBBtn
} from 'mdb-react-ui-kit';

import '../App.css';


const slides = [
  "/slideshow/hotels.png",
  "/slideshow/flow1_review_summary.png",
  "/slideshow/flow2_user_summary.png",
  "/slideshow/flow3_user-specific_review_summary.png",
  "/slideshow/flow4_real-time_new_review.png",
  "/slideshow/flow5_llm_caching.png",
  "/slideshow/monopoli.png",
];
const titles = [
  "Welcome",
  "Generic hotel summary",
  "User preferences summary",
  "User-specific hotel summary",
  "Posting a new review",
  "LLM Caching",
  "Thank you for watching",
]
const descs = [
  "Your personalized and AI-powered hotel search. Built with RAGStack and Astra DB.",
  "For each hotel, some of its reviews are condensed into a quick bullet-point summary.",
  "Users can specify their preferences, which are then made into a user-summary string.",
  "When looking at hotel details, a user-specific quick hotel description is created.",
  "New review are made available to all the app flows in real-time.",
  "A global (Astra DB-backed) cache for LLM prompt/response is quickly set up for great savings on tokens and latencies.",
  "We hope you enjoyed this small slideshow.",
]

const HomeComponent = () => {

  const [slide, setSlide] = useState(0);

  return (
    <MDBCard>
      <MDBCardImage src={slides[slide]} position='top' className="slideImage" />
      <MDBCardBody>
        <MDBCardTitle>{titles[slide]} ({1+ (slide % slides.length)} / {slides.length})</MDBCardTitle>
        <MDBCardText>
          {descs[slide]}
        </MDBCardText>
        <MDBBtn
          onClick={ () => setSlide(s => (s+1) % slides.length) }
        >
          Next
        </MDBBtn>
      </MDBCardBody>
    </MDBCard>
  );

}

export default HomeComponent
