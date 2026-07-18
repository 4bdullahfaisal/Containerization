\# Docker Task 1



A simple web application containerized with Docker using Nginx.



\## 📋 Prerequisites



\- Docker installed on your system

\- Basic knowledge of Docker commands



\## 🏗️ Project Structure



```

docker-task1/

├── index.html

└── Dockerfile

```



\## 📦 What's Inside



\- \*\*index.html\*\*: Custom HTML web page

\- \*\*Dockerfile\*\*: Docker configuration file using Nginx Alpine image



\## 🔧 Dockerfile Details



```dockerfile

FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

```



\## 🚀 Build the Docker Image



Open a terminal in the `docker-task1` folder and run:



```bash

docker build -t docker-task1 .

```



\## 🏃 Run the Container



```bash

docker run -d -p 8080:8080 docker-task1

```



\## ✅ Test the Application



Open your browser and navigate to:



```

http://localhost:8080

```



You should see your custom HTML page!



\## 🛠️ Additional Docker Commands



\### View running containers

```bash

docker ps

```



\### Stop the container

```bash

docker stop <container-id>

```



\### Remove the container

```bash

docker rm <container-id>

```



\### Remove the image

```bash

docker rmi docker-task1

```



\## 📝 Notes



\- The container runs on port 8080

\- Nginx Alpine is used for a lightweight image

\- The HTML page is served from the default Nginx directory



