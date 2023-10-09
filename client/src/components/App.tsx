import {useState} from "react";
import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarToggler,
  MDBIcon,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBCollapse,
} from 'mdb-react-ui-kit';

import './App.css';

import SiteContents from './SiteContents';
import HomeComponent from './pages/HomeComponent';
import LoginComponent from './pages/LoginComponent';

import {NavPage} from "../interfaces/enums";

function App() {

  const [userId, setUserId] = useState<string>();
  const [currentNavPage, setCurrentNavPage] = useState<NavPage>("home");

  const [showNavBarBasic, setShowNavBarBasic] = useState(false);

  return (
    <div className="App">
      <MDBNavbar expand='lg' light bgColor='light'>
        <MDBContainer fluid>
          <MDBNavbarBrand>
            <img
              src='/mono.png'
              height='30'
              alt=''
              loading='lazy'
            />
          </MDBNavbarBrand>

          <MDBNavbarToggler
            onClick={() => setShowNavBarBasic(!showNavBarBasic)}
          >
            <MDBIcon icon='bars' fas />
          </MDBNavbarToggler>

          <MDBCollapse navbar show={showNavBarBasic}>
            <MDBNavbarNav className='mr-auto mb-2 mb-lg-0'>

              <MDBNavbarItem>
                <MDBNavbarLink
                  active={currentNavPage === "home"}
                  onClick={() => setCurrentNavPage("home")}
                >
                  Home
                </MDBNavbarLink>
              </MDBNavbarItem>

              <MDBNavbarItem>
                <MDBNavbarLink
                  active={currentNavPage === "hotel_search" || currentNavPage === "hotel_details"}
                  disabled={!userId}
                  onClick={() => setCurrentNavPage("hotel_search")}
                >
                  Search
                </MDBNavbarLink>
              </MDBNavbarItem>

              <MDBNavbarItem>
                <MDBNavbarLink
                  active={currentNavPage === "user_preferences"}
                  disabled={!userId}
                  onClick={() => setCurrentNavPage("user_preferences")}
                >
                  Preferences
                </MDBNavbarLink>
              </MDBNavbarItem>

              { userId && <>
                <MDBNavbarItem className="ms-md-auto">
                  <MDBNavbarLink
                    disabled={!userId}
                    onClick={() => {setUserId(undefined); setCurrentNavPage("home");}}
                  >
                    Logout ({userId})
                  </MDBNavbarLink>
                </MDBNavbarItem>
              </> }
              { !userId && <>
                <MDBNavbarItem className="ms-md-auto">
                  <MDBNavbarLink
                    disabled={!!userId}
                    onClick={() => {setCurrentNavPage("login");}}
                  >
                    Login
                  </MDBNavbarLink>
                </MDBNavbarItem>
              </> }

            </MDBNavbarNav>
          </MDBCollapse>
        </MDBContainer>
      </MDBNavbar>

      <MDBContainer className="d-flex justify-content-center align-items-center">

        { (currentNavPage === "home") && <>
          <HomeComponent />
        </> }
        { (currentNavPage === "login") && <>
          <LoginComponent
            setUserId={setUserId}
            setCurrentNavPage={setCurrentNavPage}
          />
        </> }

      </MDBContainer>


      <div className="App-body">
        <SiteContents
          userId={userId}
          currentNavPage={currentNavPage}
          setCurrentNavPage={setCurrentNavPage}
        />
      </div>
    </div>
  );
}

export default App;
