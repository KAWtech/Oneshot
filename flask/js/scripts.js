document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
});


document.getElementById('process-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let formData = new FormData();
    let images = document.getElementById('images').files;
    for (let i = 0; i < images.length; i++) {
        formData.append('images', images[i]);
    }
    
    fetch('/process_images', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('opensplat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let formData = new FormData(this);
    let jsonData = {};
    
    formData.forEach((value, key) => jsonData[key] = value);
    jsonData.images = jsonData.images.split(',').map(image => image.trim());
    
    fetch('/process_opensplat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.message;
    })
    .catch(error => console.error('Error:', error));
});
