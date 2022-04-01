
docker build -t "rssinn" .

docker run -it --rm -p 28085:28085 rssinn
