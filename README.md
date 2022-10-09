# Installation and launch

**Installation**

You can clone this application:

```bash 
git clone https://github.com/Blastz13/TestTaskMGTU
```

**Launch**

Change directory from web app, create and apply migrations:
```bash
cd TestTaskMGTU
docker-compose up
```
OR
```bash
cd TestTaskMGTU
pip3 install -r requirements.txt
```

Now you can start the server:

```bash
uvicorn main:app --reload
```

**Swagger**

```bash
http://0.0.0.0:8000/docs
```

### License

Copyright © 2021 [Blastz13](https://github.com/Blastz13/).