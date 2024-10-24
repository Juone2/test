import requests

def ping_heroku():
    url = "https://sailrmoon.herokuapp.com"
    try:
        response = requests.get(url)
        print(f"Pinged Heroku: {response.status_code}")
    except Exception as e:
        print(f"Failed to ping Heroku: {e}")

if __name__ == "__main__":
    ping_heroku()
