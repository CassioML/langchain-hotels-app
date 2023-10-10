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
  "/slideshow/monopoli.png",
  "/slideshow/monopoli.png",
  "/slideshow/monopoli.png",
];
const titles = [
  "Welcome",
  "Diagram",
  "Diagram",
]
const descs = [
  "Your personalized and AI-powered hotel search. Built with LangChain and Astra DB.",
  "Here a diagram (todo) ...",
  "Another diagram (todo) ...",
]

const HomeComponent = () => {

  const [slide, setSlide] = useState(0);

  return (
    <MDBCard>
      <MDBCardImage src={slides[slide]} position='top' />
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
