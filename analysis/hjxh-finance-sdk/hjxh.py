import yaml

from sdk.client import Client
from settings import CONFIG_PATH

account = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.SafeLoader)['accounts']['hjxh_normal']

client = Client(account['sid'], account['appkey'], account['appsecret'])