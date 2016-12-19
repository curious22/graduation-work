# Project for graduate work

## Requirements
- Python 3
- Scrapy 1.2.1
- MongoDB 3.4.0
- Redis
- Falcon 1.1.0

```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev
```

### Run from virtual environment

Navigate into `falcon_api/`

Run command `gunicorn app`


### Run from docker container
> Doesn't completed

Pull redis and mongodb containers
```
docker pull redis
docker pull mongo
```

Run redis and mongodb
```
docker run -p 27017:27017 -v /home/$(user)/data:/data/db -d mongo # Run MongoDB
docker run -p 6379:6379 -v /docker/host/dir:/data --name docker-redis -d redis # Run Redis
```

Navigate to project root dir
```
docker run --rm -it -v $(pwd):/app 0e0a32ccc5fa sh -c 'cd /app/falcon_api/ && gunicorn app'
```


> API's endpoints are [here](docs/endpoints.md)