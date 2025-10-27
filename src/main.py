import authentication
from bs4 import BeautifulSoup as BS
import json
import requests
import os

import globals
import course

fileDir = os.path.dirname(__file__)

def getSecrets():
    with open(f'{fileDir}/../secrets.json', 'r') as f:
        data = f.read()
    return json.loads(data)

def getCourseConfig():
    with open(f'{fileDir}/../course_config.json', 'r') as f:
        data = f.read()
    return json.loads(data)

def initcourses(session : requests.Session, config):
    courses = []
    
    r = session.get(
        'https://digicampus.uni-augsburg.de/dispatch.php/my_courses',
        headers=globals.base_headers
    )
    soup = BS(r.text, 'html.parser').findAll('script')[4]
    
    coursejson = soup.text[31:-1]
    coursedata = json.loads(coursejson)['courses']
    
    cousetitles = {coursedata[d]['name']: d for d in coursedata}
    
    for c in config:
        if c['name'] in cousetitles:
            courses.append(course.Course(c['path'], cousetitles[c['name']], c['name']))
    
    return courses

def main():
    secrets = getSecrets()
    config = getCourseConfig()
    session = authentication.login(secrets['username'], secrets['password'], secrets['totpkey'])
    courses = initcourses(session, config)
    for c in courses:
        c.update(session)
    
if __name__ == '__main__':
    main()