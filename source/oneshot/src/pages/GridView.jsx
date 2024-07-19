import React, { useState, useEffect } from 'react';
import { IoAddCircleSharp } from "react-icons/io5";
import { Card, CardContent, CardMedia, CardActions, Button, Typography, Grid, IconButton, Modal, Box, TextField } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import "../styles/GridView.css";

const GridView = () => {
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState('');
  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState('');
  const [taskNumber, setTaskNumber] = useState(8000); // State for task number
  const [taskInfo, setTaskInfo] = useState({}); // State for task info
  const [uploadOk, setUploadOk] = useState(false); // State to track upload status

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
  const handleCloseModal = () => {
    setShowModal(false);
    setUploadOk(false); // Reset upload status on modal close
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      if (response.ok) {
        setUploadOk(true);
      }
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
        <Grid container spacing={5} sx={{ marginTop: '5px'}}>
            {/* Default Card */}
            <Grid item>
            <Card
              sx={{ width: 299, height: 300, display: 'flex', flexDirection: 'column', backgroundColor: '#f9f9f9', position: 'relative', justifyContent: 'center', alignItems: 'center', cursor: 'pointer' }}
              onClick={handleShowModal}
            >
              <IoAddCircleSharp size={50} />
              <Typography variant="h6">Add New Task</Typography>
            </Card>
          </Grid>
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
      <Modal
        open={showModal}
        onClose={handleCloseModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={modalStyle}>
          <IconButton
            aria-label="close"
            onClick={handleCloseModal}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Create Task
          </Typography>
          <form id="upload-form" encType="multipart/form-data" onSubmit={handleUpload} style={{ marginTop: '16px' }}>
            <input type="file" name="images" id="images" multiple required />
            <Box sx={{ mt: 2 }}>
              <Button type="submit" variant="contained" color="primary">
                Upload Images
              </Button>
            </Box>
          </form>
          {uploadOk && (
            <form id="submit-form" onSubmit={handleProcess}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="taskname"
                label="Task Name"
                name="taskname"
                autoComplete="taskname"
                autoFocus
                value={taskName}
                onChange={(e) => setTaskName(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="tasknumber"
                label="Gaussian Splat Iterations"
                type="number"
                id="tasknumber"
                autoComplete="tasknumber"
                value={taskNumber}
                onChange={(e) => setTaskNumber(Number(e.target.value))}
                inputProps={{ min: 200, max: 100000 }}
              />
              <Box sx={{ mt: 2 }}>
                <Button id="run-button" type="submit" variant="contained" color="primary">
                  Run Task
                </Button>
              </Box>
            </form>
          )}
        </Box>
      </Modal>
    </div>
  );
};

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  borderRadius: 2,
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'column',
  gap: 2,
};

export default GridView;