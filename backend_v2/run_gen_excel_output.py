import datetime
import os
import sys

import numpy as np
import pandas as pd
import pymongo

COLL_ORDERS = 'orders'
COLL_AD_SEARCH = 'ad_search'
COLL_AD_SCENE = 'ad_scene'
COLL_AD_FANGXIN = 'ad_fangxin'
COLL_GOODS_EVALUATE = 'goods_evaluate'
COLL_GOODS_DETAIL = "goods_detail"

MONGO_URI = "mongodb://hjxh-operator:hjxh-operator@212.64.67.85:2708/hjxh-operate-2"
MONGO_DB_NAME = 'hjxh-operate-2'

SHEET_NAME_1 = '单品销售（按SKU）'
T1_COLS_STAT = ['订单量', '销售金额（含税）', '退款金额', '退款占比',
                '推广成交金额占比', '多多搜索', '多多场景', '其他推广',
                '免费流量占比', '免费订单占比']

SHEET_NAME_2 = '付费推广'
T2_H1_COLORS = ['#628FCF', '#4CAFEA', '#7EAA55']
T2_H1_COLS = ['多多搜索', '多多场景', '放心推']
T2_H2_COLS = ['流量', '销量', '成交额', '花费', '点击率', '转化率', '投产']
T2_N = len(T2_H2_COLS)
T2_COLS_STAT = ['总流量', '总销量', '总花费']

SHEET_NAME_3 = '综合分析'
T3_COLS = ['流量', '转化', '金额', '销量',
           '流量', '流量占比', '转化', '销量', '销量占比',
           '流量', '流量占比', '转化', '销量', '销量占比',
           '退款金额', '退款占比']


def download_excel(mall_name: str, id: int, s_date: str, e_date: str):
    id = int(id)

    #  utc offset
    s_time = datetime.datetime.fromisoformat(s_date).timestamp()
    e_time = datetime.datetime.fromisoformat(e_date).timestamp()

    print('connecting to mongodb...')
    uri = pymongo.MongoClient(MONGO_URI)
    db = uri[MONGO_DB_NAME]
    print('connected to mongodb.')

    """
    初始数据（不要重复运行，很慢）
    """
    print('获取订单数据中……')
    # 所有正常交易的表 （184630）
    df = pd.DataFrame((db[COLL_ORDERS].find(
        {"$and": [
            {"goods_id": id},
            {"order_time": {"$gte": s_time}},
            {"order_time": {"$lte": e_time}},
            {"order_status_str": {"$not": {"$in": ["待支付", "已取消"]}}}
        ]},
        {
            'spec': 1,
            'order_status_str': 1,
            'targetDate': 1,
            'amount': {"$divide": ['$order_amount', 100]},
            "number": "$goods_number"
        }
    )))
    print('订单数据获取完成，维度：', df.shape)
    if df.shape[0] == 0:
        return None

    """
    汇总表部分
    """
    df_refund = df[df.order_status_str.str.match('.*退款成功') == True]  # 退款的表 （15338 / 184630)
    col_sum_amount = df.groupby('targetDate')['amount'].sum()  # 交易额汇总
    col_sum_volume = df.groupby('targetDate')['number'].sum()  # 交易量汇总
    col_sum_refund = df_refund.groupby('targetDate')['amount'].sum()  # 退款金额汇总
    col_refund_pct = (col_sum_refund / col_sum_amount).apply("{:.2%}".format)  # 退款金额占比

    """
    透视表部分
    """
    # 交易量透视表
    df_volume = df.pivot_table(index='targetDate', columns='spec', values='number', aggfunc='sum')
    # 交易量占比透视表
    df_volume_pct = df_volume.apply(lambda x: (x / col_sum_volume).map('{:.2%}'.format))
    # 交易额透视表
    # df_amount = df.pivot_table(index='targetDate', columns='spec', values='amount', aggfunc='sum')
    n_sku = len(df_volume.columns)
    print('SKU 数目：', n_sku)

    df1 = df_volume.join(df_volume_pct, rsuffix='_pct')
    df1 = df1.reindex(sorted(df1.columns), axis=1)
    df1['sum_volume'] = col_sum_volume
    df1['sum_amount'] = col_sum_amount
    df1['sum_refund'] = col_sum_refund
    df1['refund_pct'] = col_refund_pct

    """
    推广表
    """

    def get_ad_of_coll(coll_name: str) -> pd.Series:
        df_ad = pd.DataFrame(db[coll_name].find(
            {"$and": [
                {"goodsId": id},
                {"targetDate": {"$gte": s_date}},
                {"targetDate": {"$lte": e_date}}
            ]},
            {'gmv': 1, "_id": 0, 'targetDate': 1}
        )).groupby('targetDate')['gmv'].sum() / 1000
        return df_ad

    ad_search_gmv_sum = get_ad_of_coll(COLL_AD_SEARCH)
    ad_scene_gmv_sum = get_ad_of_coll(COLL_AD_SCENE)
    ad_fangxin_gmv_sum = get_ad_of_coll(COLL_AD_FANGXIN)
    df1['ad_gmv_pct'] = ((ad_search_gmv_sum + ad_scene_gmv_sum + ad_fangxin_gmv_sum) / col_sum_amount).apply(
        '{:.2%}'.format)
    df1['ad_search_gmv_sum'] = ad_search_gmv_sum
    df1['ad_scene_gmv_sum'] = ad_scene_gmv_sum
    df1['ad_fangxin_gmv_sum'] = ad_fangxin_gmv_sum

    def calc_ad_item(coll_name: str, goods_id: int, s_date: str, e_date: str):
        return db[coll_name].aggregate([
            {
                "$match": {
                    "$and": [
                        {"goodsId": goods_id},
                        {"targetDate": {"$gte": s_date}},
                        {"targetDate": {"$lte": e_date}}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$targetDate",
                    "flow": {"$sum": "$click"},  # 点击量
                    "impression": {"$sum": "$impression"},  # 曝光量
                    "volume": {"$sum": "$orderNum"},  # 成交笔数
                    "gmv": {"$sum": "$gmv"},  # 交易额
                    "spend": {"$sum": "$spend"}  # 花费
                }
            },
            # 花费要除以100，流量要除以100，成交额要除以1000
            {
                "$addFields": {
                    "spend": {"$divide": ["$spend", 1000]},
                    "gmv": {"$divide": ["$gmv", 1000]}
                }
            },
            {
                "$addFields": {
                    "date": "$_id",
                    "_ctr": {  # 点击率 = 点击量 / 曝光量
                        "$cond": [{"$eq": ["$impression", 0]}, 0, {"$divide": ["$flow", "$impression"]}]
                    },
                    "_cvr": {  # 转化率 = 成交笔数 / 点击量
                        # "$divide": ['$orderNum', "$click"]
                        "$cond": [{"$eq": ["$flow", 0]}, 0, {"$divide": ["$volume", "$flow"]}]
                    },
                    "_roi": {  # 投产 = 交易额 / 花费
                        # '$divide': ['$gmv', '$spend']
                        "$cond": [{"$eq": ["$spend", 0]}, 0, {"$divide": ["$gmv", "$spend"]}]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "click": 0
                }
            }
        ])

    def handle(name):
        AD_COLUMNS = ['flow', 'volume', 'gmv', 'spend', '_ctr', '_cvr', '_roi']
        df = pd.DataFrame(calc_ad_item(name, id, s_date, e_date), columns=['date'] + AD_COLUMNS)
        df.set_index('date', inplace=True)
        df.spend = df.spend.round(2)
        df._ctr = df._ctr.apply("{:.2%}".format)
        df._cvr = df._cvr.apply("{:.2%}".format)
        df._roi = df._roi.round(2)
        df.rename(columns=dict((i, i + '_' + name) for i in AD_COLUMNS), inplace=True)
        return df

    df2 = pd.concat(map(handle, [COLL_AD_SEARCH, COLL_AD_SCENE, COLL_AD_FANGXIN]), axis=1)
    df2 = df2.sort_index().fillna(0)
    df2.drop(columns=['sum_spend'], errors='ignore')
    df2.insert(loc=0, column='sum_spend',
               value=df2.apply(lambda x: sum(j for (i, j) in x.items() if i.startswith('spend')), axis=1))
    df2.insert(loc=0, column='sum_volume',
               value=df2.apply(lambda x: sum(j for (i, j) in x.items() if i.startswith('volume')), axis=1))
    df2.insert(loc=0, column='sum_flow',
               value=df2.apply(lambda x: sum(j for (i, j) in x.items() if i.startswith('flow')), axis=1))

    """
    综合分析表
    """
    data2 = list(db[COLL_GOODS_EVALUATE].find(
        {'$and': [
            {"goodsId": id},
            {"statDate": {"$gte": s_date}},
            {"statDate": {"$lte": e_date}},
        ]},
        {
            "date": "$statDate",
            "dsr": '$avgDescRevScr1m',
            "_id": 0
        }
    ))

    assert len(data2) > 0, "商品评价数据缺失"
    df_dsr = pd.DataFrame(data2, index='date').sort_index(ascending=False).round(2)

    data_flow = db[COLL_GOODS_DETAIL].find(
        {
            "$and": [
                {"goodsId": id},
                {"targetDate": {"$gte": s_date}},
                {"targetDate": {"$lte": e_date}},
            ]
        },
        {
            "total_flow": "$goodsUv",
            "total_trans": "$goodsVcr",
            # "amount_detail": "$payOrdrAmt",
            "date": "$targetDate",
            "_id": 0
        }
    )
    df_flow = pd.DataFrame(data_flow, index='date').sort_index()
    df_flow.loc[:, 'total_flow'] = df_flow.loc[:, "total_flow"].astype(int)
    df_flow.loc[:, 'total_trans'] = df_flow.loc[:, 'total_trans'].apply("{:.2%}".format)

    df3 = df_flow.join([
        col_sum_amount.rename('total_amount'),
        col_sum_volume.rename('total_volume').astype(int)
    ])

    col_charge_volume = df2.sum_volume.rename("charge_volume").astype(int)
    col_charge_flow = df2.sum_flow.rename("charge_flow").astype(int)

    df3['free_flow'] = df3.total_flow - col_charge_flow
    df3['free_flow_pct'] = (df3.free_flow / df3.total_flow).apply("{:.2%}".format)
    df3['free_trans_pct'] = (df3.free_flow / df3.total_flow).apply("{:.2%}".format)
    df3['free_volume'] = df3.total_volume - col_charge_volume
    df3['free_volume_pct'] = (df3.free_volume / df3.total_volume).apply("{:.2%}".format)

    df3['charge_flow'] = col_charge_flow
    df3['charge_flow_pct'] = (col_charge_flow / df3.total_flow).apply("{:.2%}".format)
    df3['charge_trans_pct'] = (col_charge_volume / col_charge_flow).apply("{:.2%}".format)
    df3['charge_volume'] = col_charge_volume
    df3['charge_volume_pct'] = (col_charge_volume / df3.total_volume).apply("{:.2%}".format)

    df3['sum_refund'] = col_sum_refund
    df3['refund_pct'] = col_refund_pct
    df3['DSR'] = df_dsr

    # 先给df1更新完
    df1['free_flow_pct'] = df3['free_flow_pct']
    df1['free_volume_pct'] = df3['free_volume_pct']

    df3.rename(columns={
        'total_flow': "流量",
        'total_trans': '转化',
        'total_amount': '金额',
        'total_volume': '销量',
        'charge_flow': '流量',
        'charge_flow_pct': '流量占比',
        'charge_trans': '转化',
        'charge_volume': '销量',
        'charge_volume_pct': '销量占比',
        'free_flow': '流量',
        'free_flow_pct': '流量占比',
        'free_trans': '转化',
        'free_volume': '销量',
        'free_volume_pct': '销量占比',
        'sum_refund': '退款金额',
        'refund_pct': '退款占比',
        "DSR": "DSR"
    }, inplace=True)

    def export():
        workbook_name = f"{mall_name}-{id}.xlsx"
        workbook_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), workbook_name)
        center_format = {'align': 'center'}
        header_base_format = {'bold': True, 'align': "center", 'valign': 'center', 'text_wrap': True, **center_format}
        writer = pd.ExcelWriter(workbook_name, engine='xlsxwriter')
        wb = writer.book

        def _init_sheet(sheet_name: str):
            print('saving first sheet...')
            df1.to_excel(writer, sheet_name=sheet_name, header=False, startrow=2)  # 得先导出表，才能获取
            ws = writer.sheets[sheet_name]
            ws.set_column("A:A", 12)
            return ws

        def export_sheet_1():
            ws = _init_sheet(SHEET_NAME_1)
            columns = ['占比' if i % 2 and i < 2 * n_sku else j for i, j in
                       enumerate(df1.columns[:2 * n_sku])] + T1_COLS_STAT
            for _, col in enumerate(columns):
                ws.write(1, _ + 1, col,
                         wb.add_format(dict(**header_base_format, bg_color='#628FCF' if _ < 2 * n_sku else 'yellow')))

        def export_sheet_2():
            ws = _init_sheet(SHEET_NAME_2)
            for _, ad_type in enumerate(T2_H1_COLS):
                ws.merge_range(0, 4 + _ * T2_N, 0, 3 + (_ + 1) * T2_N, ad_type,
                               wb.add_format(
                                   dict(**center_format, bg_color=T2_H1_COLORS[_], font_color="white", font_size=16)))
            for col_num, col_key in enumerate(df2.columns.values):
                col_key = T2_COLS_STAT[col_num] if col_num < 3 else T2_H2_COLS[((col_num - 3) % T2_N)]
                col_format = wb.add_format(
                    dict(**header_base_format, bg_color='yellow') if col_num < 3 else header_base_format)
                ws.write(1, col_num + 1, col_key, col_format)

        def export_sheet_3():
            ws = _init_sheet(SHEET_NAME_3)
            ws.merge_range(0, 1, 0, 4, '综合', wb.add_format(dict(**header_base_format, bg_color='#628FCF')))
            ws.merge_range(0, 5, 0, 9, '免费', wb.add_format(dict(**header_base_format, bg_color='#A0CD63')))
            ws.merge_range(0, 10, 0, 14, '付费', wb.add_format(dict(**header_base_format, bg_color='#4EAC5B')))
            ws.merge_range(0, 15, 0, 16, '退款', wb.add_format(dict(**header_base_format, bg_color='#628FCF')))
            ws.merge_range(0, 17, 1, 17, 'DSR', wb.add_format(dict(**header_base_format, bg_color='#C9D9EE')))
            for _, name in enumerate(T3_COLS):
                ws.write(1, _ + 1, name, wb.add_format(dict(**header_base_format, bg_color='#CCD9EC')))

        export_sheet_1()
        export_sheet_2()
        export_sheet_3()
        writer.save()
        print('finished saving excel: ')
        print(workbook_path)

    export()


if __name__ == '__main__':
    MALL_NAME = "皇家小虎食品旗舰店冯露"
    DEFAULT_GOODS_ID = 221058511472
    s_date = '2021-07-19'
    e_date = '2021-07-25'
    # print(sys.argv)
    if sys.argv.__len__() == 1:
        download_excel(MALL_NAME, DEFAULT_GOODS_ID, s_date, e_date)
    else:
        download_excel(*sys.argv[1:])
