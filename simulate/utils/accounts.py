import yaml

from simulate.config.const import PATH_ACCOUNTS

accounts = yaml.load(open(PATH_ACCOUNTS, "r", encoding="utf-8"), Loader=yaml.SafeLoader)
