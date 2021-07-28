from hjxh import client
import pandas as pd

url = 'https://api.wangdian.cn/openapi2/stockout_order_query_trade.php'
params = {
    'start_time': '2021-04-29 14:00:00',
    'end_time': '2021-04-29 15:00:00',
}

data = client.query(url, params)


df = pd.DataFrame(data['stockout_list'])

print('finished')
