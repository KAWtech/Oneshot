import logo from './logo.svg';
import './App.css';
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import GridView from "./pages/GridView.jsx"
import ModelViewer from './pages/ModelViewer.jsx';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path='/' element={<GridView/>}></Route>
          <Route path='/viewer/:uuid' element={<ModelViewer/>}></Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
