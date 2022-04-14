
docker build -t "rssinn" .

docker run -it --rm -p 28085:28085 rssinn


pdm run uvicorn run:app --host 0.0.0.0 --port 8085 --reload --debug

关闭进程：
fuser -n tcp -k 8085


安装package，运行：
pdm add package

查看内存
http://www.cppcns.com/os/linux/325301.html
https://blog.csdn.net/qq_43469158/article/details/118441928
