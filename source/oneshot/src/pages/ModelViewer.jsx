import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';

const ModelViewer = () => {
    const { uuid } = useParams();

    useEffect(() => {
        // You can use the uuid here if needed
        console.log(`Loading model viewer for UUID: ${uuid}`);

        // Create an iframe to embed the viewer
        const iframe = document.createElement('iframe');
        iframe.src = `http://localhost:3001/viewer/dist/index.html`;
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';

        // Append the iframe to the container div
        const container = document.getElementById('model-viewer-container');
        container.appendChild(iframe);

        // Clean up the iframe when the component is unmounted
        return () => {
            container.removeChild(iframe);
        };
    }, [uuid]);

    return (
        <div id="model-viewer-container" style={{ width: '100%', height: '100vh' }}>
            {/* This div will be populated by the iframe */}
        </div>
    );
};

export default ModelViewer;