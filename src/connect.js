let socket = new WebSocket("ws://localhost:8787/");

socket.onopen = function(e) {
  console.log("[open] Connection established");
  console.log("Sending to server");
};

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
  
    // Parse the data received from the server
    let data = JSON.parse(event.data);
  
    // If the data contains a character, show a modal
    if (data.status === 'login success') {
        // Create a modal
        let modal = document.createElement('div');
        modal.style.display = 'block';
        modal.style.width = '200px';
        modal.style.height = '200px';
        modal.style.background = '#fff';
        modal.style.position = 'fixed';
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%)';
        modal.style.padding = '20px';
        modal.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.1)';
        
        // Create a rotating graphic
        let graphic = document.createElement('div');
        graphic.style.width = '50px';
        graphic.style.height = '50px';
        graphic.style.border = '4px solid #f3f3f3';
        graphic.style.borderTop = '4px solid #3498db';
        graphic.style.borderRadius = '50%';
        graphic.style.animation = 'spin 2s linear infinite';
        graphic.style.margin = 'auto';
        
        // Add the rotating graphic to the modal
        modal.appendChild(graphic);
        
        // Add some text to the modal
        let text = document.createElement('h2');
        text.textContent = 'Waiting for game to start...';
        modal.appendChild(text);
        
        // Append the modal to the body
        document.body.appendChild(modal);
        
        // Add the CSS for the spinning animation
        let style = document.createElement('style');
        style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        `;
        document.head.appendChild(style);
    }

  };

socket.onerror = function(error) {
  console.log(`[error] ${error.message}`);
};

// Get the form element
let form = document.getElementById('loginForm');

// Add an event listener for form submissions
form.addEventListener('submit', function(e) {
  // Prevent the form from being submitted
  e.preventDefault();

  // Get the user's channel name
  let channelName = document.getElementById('channelName').value;

  // Send the channel name to the server
  socket.send(JSON.stringify({ action: 'login', name: channelName }));
});