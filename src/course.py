import globals
import os
import json
from bs4 import BeautifulSoup as BS

BASE_URL = 'https://digicampus.uni-augsburg.de/dispatch.php/course/files'
FILE_URL = 'https://digicampus.uni-augsburg.de/sendfile.php?force_download=1&type=0'

class Folder:
    def __init__(self, path, id, cid):
        self.path = path
        self.id = id
        self.cid = cid
        
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
    
    def update(self, session):
        r = session.get(
            f'{BASE_URL}/index/{self.id}?cid={self.cid}'
        )
        soup = BS(r.text, 'html.parser')
        form = soup.find('form', {'id': 'files_table_form'})
        files = json.loads(form.get('data-files'))
        folders = json.loads(form.get('data-folders'))
        
        for folder in folders:
            Folder(f'{self.path}/{folder["name"]}', folder['id'], self.cid).update(session)
        
        for file in files:
            fullpath = f'{self.path}/{file["name"]}'
            if not os.path.exists(fullpath) or file['chdate'] > os.path.getmtime(fullpath):
                print("Downloading", file["name"])
                r = session.get(
                    file['download_url']
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
        print("Updating", self.name)
        r = session.get(
            BASE_URL + '?cid=' + self.id
        )
        soup = BS(r.text, 'html.parser')
        
        form = soup.find('form', {'id': 'files_table_form'})
        rootFolder = form.find('input', {'name':'parent_folder_id'}).get('value')
        
        Folder(self.path, rootFolder, self.id).update(session)
        
        return
