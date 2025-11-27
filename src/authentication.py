import requests
from bs4 import BeautifulSoup as BS
import pyotp
import globals

START_PAGE = "https://digicampus.uni-augsburg.de/dispatch.php/start"

def login(username, password, totpkey):
    print("🗝 Starting session")
    session = requests.Session()
    session.headers.update(globals.base_headers)
    r = session.get(
        START_PAGE
    )
    soup = BS(r.text, 'html.parser')
    link = soup.find('article', id='loginbox').find('a').get('href')
    
    r = session.get(
        link
    )
    soup = BS(r.text, 'html.parser')
    formlink = soup.find('div', class_='uaux-login-pw').find('form').get('action')
    
    r = session.post(
        formlink,
        headers=globals.additional_headers,
        data={
            'username': username,
            'password': password
        }
    )
    soup = BS(r.text, 'html.parser')
    formlink = soup.find('form').get('action')
    
    r = session.post(
        formlink,
        headers=globals.additional_headers,
        data={
            'otp': pyotp.TOTP(totpkey.replace(' ', '')).now()
        }
    )
    soup = BS(r.text, 'html.parser')
    form = soup.find('form')
    formlink = form.get('action')
    samlresponse = form.find('input').get('value')
    
    r = session.post(
        formlink,
        headers=globals.additional_headers,
        data={
            'SAMLResponse': samlresponse
        }
    )
    soup = BS(r.text, 'html.parser')
    form = soup.find('form')
    formlink = form.get('action')
    samlresponse = form.find('input', {'name': 'SAMLResponse'}).get('value')
    relaystate = form.find('input', {'name': 'RelayState'}).get('value')
    
    r = session.post(
        formlink,
        headers=globals.additional_headers,
        data = {
            'SAMLResponse': samlresponse,
            'RelayState': relaystate
        }
    )
    
    return session if r.status_code == 200 else None
