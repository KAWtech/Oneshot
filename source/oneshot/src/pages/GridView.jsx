import React, { useState, useEffect } from 'react';
import { IoAddCircleSharp } from "react-icons/io5";
import { Card, CardContent, CardMedia, CardActions, Button, Typography, Grid } from '@mui/material';
import "../styles/GridView.css";

const GridView = () => {
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState('');
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('http://localhost:5000/tasks');
        const data = await response.json();
        console.log('Fetched tasks:', data); // Debugging: Check the response
        if (Array.isArray(data)) {
          setTasks(data);
        } else {
          console.error('Unexpected data format:', data);
        }
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, []);

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
        <div className="top-bar-text">Oneshot, Ultra Fast Gaussian Splat Processing</div>
      </div>
      <div className="body-content">
        <div id="add-task-menu" className="add-task-menu">
          <div className="add-task-text">Make New Splat</div>
          <button id="add-task-button" className="add-task-button" onClick={handleShowModal}>
            <IoAddCircleSharp />
          </button>
        </div>
        <Grid container spacing={5}>
          {tasks.map((task, index) => (
            <Grid item key={index}>
              <Card sx={{ width: 299, height: 300, display: 'flex', flexDirection: 'column',  backgroundColor: '#f9f9f9', position: 'relative' }}>
                <CardMedia
                  component="img"
                  sx={{height:"140px"}}
                  image={`http://localhost:5000${task.image_url}`}
                  alt="Loading..."
                />
              <CardContent sx={{ textAlign: 'left' }}>
                <Typography gutterBottom variant="h5" component="div" sx={{ width: "267px", marginLeft: "-6px", marginTop: "-3px"}}>
                  Task Name
                </Typography>
                <Typography variant="body2" component="div" sx={{ width: "267px", paddingLeft: "6px"}}>
                  7/5/2024 @ 17:23
                </Typography>
              </CardContent>
              <CardActions sx={{ marginTop: 'auto' }}>
                <Button size="small">View Splat</Button>
                <Button size="small">Download Splat</Button>
              </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>     
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