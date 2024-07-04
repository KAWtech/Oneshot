import React, { useState } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';
import { FcAddImage } from "react-icons/fc";
import { IoAddCircleSharp } from "react-icons/io5";
import "../styles/GridView.css";

const GridView = () => {
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState('');

  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  const handleUpload = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleProcess = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/process_images', {
        method: 'POST'
      });
      const data = await response.json();
      setResult(data.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div id="wrapper">
      <div className="top-bar-background">
        <div className="top-bar-text">OneSplat, Ultra Fast Gaussian Splat Processing</div>
      </div>
      <div className="body-content">
        <div id="add-task-menu" className="add-task-menu">
          <div className="add-task-text">Make New Splat</div>
          <button id="add-task-button" className="add-task-button" onClick={handleShowModal}>
            <IoAddCircleSharp />
          </button>
        </div>
      </div>
      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <button onClick={handleCloseModal} className="close-button">&times;</button>
            <h2>Create Task</h2>
            <form id="upload-form" encType="multipart/form-data" onSubmit={handleUpload}>
              <input type="file" name="images" id="images" multiple required />
              <button type="submit">Upload Images</button>
            </form>
            <form id="submit-form" onSubmit={handleProcess}>
                <br />
               <button id="run-button">Run Task</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GridView;
