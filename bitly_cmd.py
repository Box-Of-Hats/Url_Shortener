"""A cmd application utilising bitly to shorten links"""
import requests
import os
import sys
from auth_data import AUTHENTICATION

def shorten_link(url, user, password, token):
    """Shortens a given url, requires authentication data"""
    api_url = 'https://api-ssl.bitly.com'
    get_lookup = '/v3/link/lookup?url={}&access_token={}'.format(url, token)
    this_request = requests.get('{}{}'.format(api_url, get_lookup), auth=(user, password))
    if this_request.status_code != 200:
        print('Error with request. Status Code: {}'.format(this_request.status_code))
        return False
    else:
        json = this_request.json()
        try:
            shortened_url = json['data']['link_lookup'][0]['aggregate_link']
            return shortened_url
        except KeyError:
            print('Issue parsing JSON: {}'.format(json))
            return False

def copy_to_clipboard(text):
    """Adds a given string to the clipboard"""
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

def user_input_app():
    """Takes user input"""
    print('Enter a Url to shorten using bitly.')
    url_to_shorten = input('>')
    return url_to_shorten

def main():
    """Main method"""
    #Try to locate authentication data
    for key in AUTHENTICATION:
        if AUTHENTICATION[key] == '':
            print('Could not continue.')
            print('\tMissing authentication data: {}'.format(key))
            print('Add your authentication data to the auth_data.py file.')
            quit()

    #Take user input if cmd arg not passed
    if len(sys.argv) > 1:
        url_to_shorten = sys.argv[-1]
    else:
        url_to_shorten = user_input_app()

    bitly_link = shorten_link(url_to_shorten,
                              AUTHENTICATION['username'],
                              AUTHENTICATION['password'], 
                              AUTHENTICATION['token'])

    if bitly_link:
        copy_to_clipboard(bitly_link)
        print('{} copied to clipboard'.format(bitly_link))
    else:
        print('Error with url.')
    #Wait for return to close window
    input()

if __name__ == '__main__':
    main()
