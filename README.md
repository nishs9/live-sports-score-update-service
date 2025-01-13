# LIve Sports Score Update Service

## Description

This is a set of python scripts that are used to update a Redis database with live NFL and MLB scores. it is one component of a project I have worked on using an Adafruit M4 MatrixPortal. The other component is the API which the MatrixPortal calls in order to get the data which it displays. The repository for that [can be found here](https://github.com/nishs9/live-sports-scoreboard-api).

The intention is that these scripts can be integrated with any cron job framework to keep a Redis DB (or any DB for that matter) updated with live scores from the NFL and MLB. For my project, these scripts are being deployed on a Raspberry Pi 5 and using the built-in `crontab` tool. 

## Setup [work in progress...]
In order to set this up on your machine, start by cloning this repository:

```
git clone https://github.com/nishs9/live-sports-score-update-service.git
cd live-sports-score-update-service
```

Next, set up a python virtual environment (venv) and install the dependencies from the `requirements.txt` file:

```
python3 -m venv *venv name*
pip install -r requirements.txt
```

Your next step should be to set up a Redis DB on the environment of your choice. Once you have your Redis DB ready, make a note of the Redis server's IP and port. Then, create a `proj_secrets.py` file and fill it out as shown below:

```
REDIS_SERVER_IP = *add IP heree*
REDIS_SERVER_PORT = *add port here*
```

Before moving on, you should test that the script and your Redis server are working with one another. Simply run either or both of the following commands:

```
python nfl_scores_update_script.py
python mlb_scores_update_script.py
```
