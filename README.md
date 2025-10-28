# DigiScraper

A scraper for Uni Augsburg's DigiCampus

## Functionality

DigiScraper will download all files that are found in DigiCampus but are non-existent or older on your system. This will overwrite existing files if your file is older.

### course_config.json

The courses are specified in `course_config.json`. The specification includes the course name, as well as the path where the files should be saved on your system. Directory structures are preserved.

A sample can be found at [`course_config_sample.json`](./course_config_sample.json).

### secrets.json

This file holds your secrets; your username and password, as well as the TOTP key.

A sample can be found at [`secrets_sample.json`](./secrets_sample.json).

## Setup

- Run `pip install -r requirements.txt`
- Run `python3 registertotp.py`, this will guide you through the 2fa setup process
- Enter your username and password in `secrets.json`
- Specify your courses and paths in `course_config.json`

Now you can run `python3 src/main.py`, which should refresh all your files.
