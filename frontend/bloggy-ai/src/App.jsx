import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Provider } from "react-redux";
import UserWrapper from './layout/UserWrapper.jsx';
// import AdminWrapper from './components/Admin/AdminWrapper';
import {userStore} from './redux/userStore.jsx'

function App() {

  return (
    <>
    <Router>
      <Provider store={userStore}>
      <Routes>
      <Route path="/*" element={<UserWrapper />} />
      {/* <Route path="/admin/*" element={<AdminWrapper />} /> */}
      </Routes>
      </Provider>
    </Router>
    </>
  )
}

export default App
