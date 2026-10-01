# superkart-sales-prediction
Suparkart Sales prediction project


# how to build backend docker file
/workspaces/superkart-sales-prediction => docker build -t superkart-backend ./backend

# how to run the backend docker file
docker run -d -p 7860:7860 --name superkart-container superkart-backend

# how to build frontend docker file
/workspaces/superkart-sales-prediction => docker build -t superkart-frontend ./frontend

# how to run the frontend docker file
docker run -d -p 7860:7860 --name superkart-frontend-container superkart-frontend

# how to stop and remove  the container
docker stop superkart-container
docker rm superkart-container

docker stop superkart-frontend-container
docker rm superkart-frontend-container

 
