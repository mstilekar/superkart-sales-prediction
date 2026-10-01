# superkart-sales-prediction
Suparkart Sales prediction project


# how to build docker file
/workspaces/superkart-sales-prediction => docker build -t superkart-backend ./backend

# how to run the docker file
docker run -d -p 7860:7860 --name superkart-container superkart-backend
