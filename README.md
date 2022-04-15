## docker
docker build -t "rssinn" .

docker run -it --rm -p 28085:28085 rssinn

## PDM
加入path：`export PATH=/root/.local/bin:$PATH`

pdm run uvicorn run:app --host 0.0.0.0 --port 28085 --reload --debug
pdm run daphne run:app -b 0.0.0.0 -p 28085

关闭进程： `fuser -n tcp -k 28085`


安装package，运行： `pdm add PackageName`

查看内存:
- http://www.cppcns.com/os/linux/325301.html
- https://blog.csdn.net/qq_43469158/article/details/118441928
