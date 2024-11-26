// import logo from "./logo.svg";
import "./App.css";
import React from "react";
import Login from "./components/Login/Login";
import UserDashboard from "./components/UserDashboard/UserDashboard";
// import UserRegistration from "./components/UserRegistration/UserRegistration";
// import DoctorRegistration from "./components/DoctorRegistration/DoctorRegistration";
// import PatientRegistration from "./components/PatientRegistration/PatientRegistration";

function App() {
  return (
    <div className="App">
      <Login />
      {/* <UserDashboard/> */}
      {/* <UserRegistration /> */}
      {/* <DoctorRegistration /> */}
      {/* <PatientRegistration /> */}
    </div>
    //   <div className="App">
    //     <header className="App-header">
    //       <img src={logo} className="App-logo" alt="logo" />
    //       <p>
    //         Edit <code>src/App.js</code> and save to reload.
    //       </p>
    //       <a
    //         className="App-link"
    //         href="https://reactjs.org"
    //         target="_blank"
    //         rel="noopener noreferrer"
    //       >
    //         Learn React
    //       </a>
    //     </header>
    //   </div>
  );
}

export default App;
