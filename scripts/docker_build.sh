docker build -t prize-draw:latest ../.
docker run -d -p 5000:5000 --name prize prize-draw
