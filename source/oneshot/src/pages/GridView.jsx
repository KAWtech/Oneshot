import React, { useState, useEffect } from 'react';
import { IoAddCircleSharp } from "react-icons/io5";
import { Card, CardContent, CardMedia, CardActions, Button, Typography, Grid, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import "../styles/GridView.css";

const GridView = () => {
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState('');
  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState('');
  const [taskNumber, setTaskNumber] = useState(8000); // State for task number
  const [taskInfo, setTaskInfo] = useState({}); // State for task info

  useEffect(() => {
    const fetchTaskInfo = async () => {
      try {
        const response = await fetch('http://localhost:5000/task_info');
        const data = await response.json();
        setTaskInfo(data);
      } catch (error) {
        console.error('Error fetching task info:', error);
      }
    };

    fetchTaskInfo();
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

    const today = new Date();
    const month = today.getMonth() + 1;
    const year = today.getFullYear();
    const date = today.getDate();
    const hours = today.getHours();
    const minutes = today.getMinutes();
    const seconds = today.getSeconds();
    const currentDate = month + "/" + date + "/" + year + " @ " + hours + ":" + minutes + ":" + seconds;
    try {
      const response = await fetch('http://localhost:5000/process_images', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ taskName, taskNumber: taskNumber.toString(), currentDate }) // Include the task name & date
      });
      const data = await response.json();
      setResult(data.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDelete = async (taskId) => {
    try {
      const response = await fetch(`http://localhost:5000/delete_task/${taskId}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        // Remove the task from the taskInfo state
        const updatedTaskInfo = { ...taskInfo };
        delete updatedTaskInfo[taskId];
        setTaskInfo(updatedTaskInfo);
      } else {
        console.error('Failed to delete task:', response.statusText);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleDownload = (taskId) => {
    const url = `http://localhost:5000/download_splat/${taskId}`;
    window.open(url, '_blank');
  };

  const openInNewTab = (url) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div id="wrapper">
      <div className="top-bar-background">
        <div className="top-bar-text">
          <span className="text-big">Oneshot</span>
          <span className="text-small">Ultra Fast Gaussian Splat Processing</span>
        </div>
      </div>
      <div className="body-content">
        <div id="add-task-menu" className="add-task-menu">
          <div className="add-task-text">Make New Splat</div>
          <button id="add-task-button" className="add-task-button" onClick={handleShowModal}>
            <IoAddCircleSharp />
          </button>
        </div>
        <Grid container spacing={5}>
          {Object.entries(taskInfo).map(([uuid, info]) => (
            <Grid item key={uuid}>
              <Card sx={{ width: 299, height: 300, display: 'flex', flexDirection: 'column',  backgroundColor: '#f9f9f9', position: 'relative' }}>
                <CardMedia
                  component="img"
                  sx={{height:"170px"}}
                  image={`http://localhost:5000/data/${uuid}/images/0.jpg`} // Assuming the image_url is part of taskInfo
                  alt=""
                />
                <CardContent sx={{ textAlign: 'left' }}>
                                  <IconButton
                  aria-label="delete"
                  sx={{ position: 'absolute', top: 170, right: 0 }}
                  onClick={() => handleDelete(uuid)}
                >
                  <CloseIcon />
                </IconButton>
                  <Typography gutterBottom variant="h5" component="div" sx={{ width: "267px", marginLeft: "-6px", marginTop: "-3px"}}>
                    {info.taskname || 'Unnamed Task'}
                  </Typography>
                  <Typography variant="body2" component="div" sx={{ width: "267px", paddingLeft: "6px"}}>
                    {info.taskdate || 'Date not available'}
                  </Typography>
                </CardContent>
                <CardActions sx={{ marginTop: 'auto' }}>
                  <Button size="small" onClick={() => openInNewTab('/viewer/' + uuid)}>View Splat</Button>
                  <Button size="small" onClick={() => handleDownload(uuid)}>Download Splat</Button>
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
            <form id="upload-form" encType="multipart/form-data" onSubmit={handleUpload} style={{ textAlign: 'left' }}>
              <input type="file" name="images" id="images" multiple required style={{ paddingLeft: "40px", paddingBottom: "10px" }}/>
              <br />
              <div style={{ paddingLeft: "40px", paddingBottom: "10px" }}>
                <button type="submit">Upload Images</button>
              </div>
              <span style={{ paddingLeft: "40px", paddingBottom: "10px" }}>Task Name</span>
              <div style={{ paddingLeft: "40px", paddingBottom: "10px" }}>
                <input type="text" name="taskname" id="taskname" value={taskName} onChange={(e) => setTaskName(e.target.value)} required/>
              </div>
              <span style={{ paddingLeft: "40px", paddingBottom: "10px" }}>Gaussian Splat Iterations</span>
              <div style={{ paddingLeft: "40px", paddingBottom: "10px" }}>
                <input type="number" name="tasknumber" id="tasknumber" value={taskNumber} onChange={(e) => setTaskNumber(Number(e.target.value))} min="200" max="100000" required />
              </div>
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