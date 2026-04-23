import os
from bs4 import BeautifulSoup as BS
import datetime

BASE_URL = 'https://digicampus.uni-augsburg.de'
API_URL = 'https://digicampus.uni-augsburg.de/jsonapi.php/v1'

class Folder:
    def __init__(self, path, id, relpath, indent):
        self.path = path
        self.id = id
        self.relpath = relpath
        self.indent = indent
        
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
    
    def update(self, session):
        print(f'{"  " * self.indent}🖿 Updating {self.relpath}')
        r = session.get(
            f'{API_URL}/folders/{self.id}/folders?page[limit]=2000'
        )
        
        for folder in r.json()['data']:            
            Folder(f'{self.path}{os.sep}{folder['attributes']['name']}', folder['id'], folder['attributes']['name'], self.indent + 1).update(session)
            
        r = session.get(
            f'{API_URL}/folders/{self.id}/file-refs?page[limit]=2000'
        )
        
        for file in r.json()['data']:
            if not file['attributes']['is-downloadable']:
                continue
        
            fullpath = f'{self.path}{os.sep}{file['attributes']['name']}'
            if not os.path.exists(fullpath) or datetime.datetime.fromisoformat(file['attributes']['chdate']).timestamp() > os.path.getmtime(fullpath):
                print(f'{"  " * (self.indent + 1)}⬇ {"Downloading" if not os.path.exists(fullpath) else "Updating"} {file["attributes"]["name"]}')
                
                r = session.get(
                    f'{BASE_URL}{file['meta']['download-url']}'
                )
                
                with open(fullpath, 'wb+') as f:
                    f.write(r.content)
        
        return
        

class Course:
    
    def __init__(self, path, id, name):
        self.path = path
        self.id = id
        self.name = name
    
    def update(self, session):
        r = session.get(
            f'{API_URL}/courses/{self.id}/folders'
        )
        
        rootFolderId = [f['id'] for f in r.json()['data'] if f['attributes']['folder-type'] == 'RootFolder'][0]
        
        Folder(self.path, rootFolderId, self.name, 0).update(session)
        
        return
