# React + Node.js Multi-Container Setup

This project demonstrates a multi-container Docker setup with a React frontend and Node.js backend using Docker Compose.

## Project Structure

```
react-node-app/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── (React app)
└── backend/
    ├── Dockerfile
    └── (Node.js app)
```

### Setup Instructions

1. **Clone or create the project structure**

```bash
mkdir react-node-app
cd react-node-app
```

2. **Create the backend**

```bash
mkdir backend
cd backend
```

Create `package.json`:
```json
{
  "name": "backend",
  "version": "1.0.0",
  "description": "Node.js backend",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  }
}
```

Create `server.js`:
```javascript
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Backend!' });
});

app.get('/api/users', (req, res) => {
  res.json([
    { id: 1, name: 'John Doe' },
    { id: 2, name: 'Jane Smith' }
  ]);
});

app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
```

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm", "start"]
```

Return to root:
```bash
cd ..
```

3. **Create the frontend**

```bash
npx create-react-app frontend
cd frontend
```

Replace `src/App.js` with:
```javascript
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/hello')
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => console.log(err));

    fetch('http://localhost:5000/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React + Node.js Docker App</h1>
        <p>Backend says: <strong>{message || 'Loading...'}</strong></p>
        <h3>Users:</h3>
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
```

Replace `src/App.css` with:
```css
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background: #61dafb;
  color: #282c34;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
}
```

Create `Dockerfile` in frontend folder:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Return to root:
```bash
cd ..
```

4. **Create docker-compose.yml** in the root folder

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: node-backend
    restart: unless-stopped
    ports:
      - "5000:5000"
    networks:
      - app-network

  frontend:
    build: ./frontend
    container_name: react-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Running the Application

Build and start the containers:

```bash
docker-compose up -d --build
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api/hello

## Stopping the Application

```bash
docker-compose down
```

---
