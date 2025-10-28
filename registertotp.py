#!/usr/env/python
import json
import os
import pyotp

def main():
    print('Go to https://auth.rz.uni-augsburg.de/realms/uaux/account/account-security/signing-in and set up a Two-Factor authenticator.')
    print('On the page that shows you a QR code, click on "Unable to scan?", and enter the key here:')
    totpkey = input()
    try:
        print('Enter the following One-time code:', pyotp.TOTP(totpkey.replace(' ', '')).now())
    except:
        print('Invalid key, try again.')
        return
    
    if not os.path.exists('secrets.json'):
        with open('secrets.json', 'w+') as f:
            json.dump({'totpkey': totpkey, 'username': 'your RZ-ID', 'password': 'your RZ_ID password'}, f, indent=2)
    else:
        with open('secrets.json', 'r') as f:
            data = json.load(f)
        data['totpkey'] = totpkey
        with open('secrets.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    print('Done.')

if __name__ == '__main__':
    main()