import requests
import os
from dotenv import load_dotenv
import argparse
load_dotenv()

def create_bitlink(long_url, api_token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    data = {"long_url": long_url}
    headers = {"Authorization": "Bearer {}".format(api_token)}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def get_clickings(api_token):
    payload= {
      'unit':'day',
      'units':-1
    }
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(formatted_url)
    headers = {"Authorization": "Bearer {}".format(api_token)}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()


def check_bitlink(api_token):
    payload= {
    }
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(formatted_url)
    headers = {"Authorization": "Bearer {}".format(api_token)}
    response = requests.get(url, headers=headers, params=payload)
    return response.ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL is the URL by which you want to create a bit link or get the total number of clicks")
    args = parser.parse_args()
    args_url = args.url
    api_token = os.getenv("token")
    formatted_url = args_url.split('//')[-1]
    if check_bitlink(api_token):
        total_clicks = get_clickings(api_token)["total_clicks"]
        print("общее количество переходов:", total_clicks)
    else:
        if args_url.startswith('http'):
            long_url = args_url
        else:
            long_url = 'http://{}'.format(formatted_url)
        data_from_url = create_bitlink(long_url, api_token)
        received_bit_link =data_from_url.get('link')
        if received_bit_link:
            print(received_bit_link)
        else:
            print('broken link')
