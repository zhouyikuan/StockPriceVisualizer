from rauth import OAuth1Service as oauth
from pathlib import Path
import configparser

config = configparser.ConfigParser()
apiSecretsPath = Path.cwd() / 'StockPriceVisualizer/APISecrets'
configLocation = apiSecretsPath / 'apiKey.ini' # If error, check project directory
config.read(configLocation)
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

# Step 1
# retrieve request token and request token secret
request_token, request_token_secret = etrade.get_request_token(
    params={"oauth_callback": "oob", "format": "json"}
)

# Step 2: Verification Link
authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
print(authorize_url)

print("Access the URL and enter code here:")
oauth_verifier = input()

authKeys = open(apiSecretsPath / 'accessToken.ini','w')
access_token = etrade.get_access_token(request_token, request_token_secret, params={"oauth_verifier": oauth_verifier})
print(access_token)
authKeys.write("[ACCESS_TOKEN]\nf=" + access_token[0] + "\ns=" + access_token[1])
authKeys.close()
print("Credentials updated")