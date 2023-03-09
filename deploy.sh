tag=$1

docker build -f Dockerfile -t operationstool:$tag .
docker tag operationstool:$tag xxx.xxx.xxx.xxx/devops/operationstool:$tag
docker push xxx.xxx.xxx.xxx/devops/operationstool:$tag
