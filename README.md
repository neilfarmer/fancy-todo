# Fancy Todo

This is a simple todo application. It saves task information locally so the application can be blown away and redeployed with the same taks information

You can build this yourself or pull from Docker Hub

```sh
docker run -p 5001:5001 \
    -e DATA_DIR=$(DATA_DIR) \
    -v $$(pwd)/$(DATA_DIR):/app/data \
    --name todo-flask-app \
    nfarmer371/fancy-todo:latest
```

| Environment Variable | Explanation                                  | Default |
| -------------------- | -------------------------------------------- | ------- |
| DATA_DIR             | Directory where task data is stored locally. | ./data  |
