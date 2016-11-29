# Test project: MongoDB + falcon

## Run
```
gunicorn test_app/app
```

## Testing
```
http localhost:8000/status?completed
http localhost:8000/status?skipped
http localhost:8000/status?fkejfekwljf
```
