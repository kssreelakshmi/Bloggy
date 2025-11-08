import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from  '../Pages/User/Home.jsx'
import Signup from '../Pages/User/Signup.jsx'
import Home from '../Pages//User/Login.jsx' 
import Profile from '../Pages//User/Profile.jsx' 

const UserWrapper = () => {
  return (
    <>
    <Router>

    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        
    </Routes>

    </Router>

    </>
  )
}

export default UserWrapper