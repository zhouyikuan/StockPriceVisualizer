from rauth import OAuth1Service as oauth
from pathlib import Path
import configparser
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

config = configparser.ConfigParser()
apiSecretsPath = Path.cwd() / 'StockPriceVisualizer/APISecrets'
config.read(apiSecretsPath / 'apiKey.ini')

state = 1 # 0 sandbox #1 prod
if state:
    base_url = config["CONSUMER"]["PROD_BASE_URL"]
else:
    base_url = config["CONSUMER"]["SANDBOX_BASE_URL"]

etrade = oauth(
    name="etrade",
    consumer_key=config["CONSUMER"]["KEY"],
    consumer_secret=config["CONSUMER"]["SECRET"],
    request_token_url=config["DEFAULT"]["REQUEST_TOKEN_URL"],
    access_token_url=config["DEFAULT"]["ACCESS_TOKEN_URL"],
    authorize_url=config["DEFAULT"]["AUTHORIZE_URL"],
    base_url=config["DEFAULT"]["BASE_URL"]
)

config.read(apiSecretsPath / 'accessToken.ini')

session = etrade.get_session(token = (config["ACCESS_TOKEN"]["f"], config["ACCESS_TOKEN"]["s"] ))

temp = base_url + "/v1/market/quote/" + "META" + ".json"
te = session.get(temp)
print(te.text)