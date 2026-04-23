#!/usr/bin/env python
import authentication
import json
import requests
import os

import course

API_URL = 'https://digicampus.uni-augsburg.de/jsonapi.php/v1'

fileDir = os.path.dirname(__file__)

def getSecrets():
    with open(os.path.abspath(os.sep.join([fileDir, '..', 'secrets.json'])), 'r') as f:
        data = f.read()
    return json.loads(data)

def getCourseConfig():
    with open(os.path.abspath(os.sep.join([fileDir, '..', 'course_config.json'])), 'r') as f:
        data = f.read()
    return json.loads(data)

def initcourses(session : requests.Session, config):
    courses = []
    
    r = session.get(
        f'{API_URL}/users/me'
    )
    
    userId = r.json()['data']['id']
    
    r = session.get(
        f'{API_URL}/users/{userId}/courses?page[limit]=2000'
    )
    
    courseJson = r.json()['data']
    
    confignames = {c['name']: c['path'] for c in config}
    
    for c in courseJson:
        if c['attributes']['title'] in confignames:
            courses.append(course.Course(confignames[c['attributes']['title']], c['id'], c['attributes']['title']))
    
    return courses

def main():
    secrets = getSecrets()
    config = getCourseConfig()
    try:
        session = authentication.login(secrets['username'], secrets['password'], secrets['totpkey'])
    except:
        print("⨯ Could not start session.\n")
        exit(1)
    courses = initcourses(session, config)
    for c in courses:
        c.update(session)
    print("✔ Done.\n")
    
if __name__ == '__main__':
    main()