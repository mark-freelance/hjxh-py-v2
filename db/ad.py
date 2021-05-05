from datetime import datetime

import pandas as pd

from db.client import db
from settings import KEY_AD_ID, AD_MAP, EPS

coll_ad = db['ad']


def get_ad_from_doc(doc):
    return dict((i, doc.get(AD_MAP[i], None)) for i in AD_MAP)


def get_ads():
    """
    ['221058511472',
     '227697595376',
     '228510019255',
     '228871185592',
     '231373336107',
     '233304230883',
     '236506450340']
    :return:
    """
    return coll_ad.distinct(KEY_AD_ID)


def str2number(s: str):
    if pd.isna(s):
        return pd.NA
    return float(s.replace(",", ""))


def convert2normal(val: any):
    if pd.isna(val):
        return None
    else:
        return val


def get_ad_info(df):
    baoguangliang = df['曝光量'].apply(str2number).sum()
    liuliang = df['点击量'].apply(str2number).sum()
    dianjilv = liuliang / baoguangliang if baoguangliang else 0
    chengjiaobishu = df['成交笔数'].apply(str2number).sum()
    zhuanhua = chengjiaobishu / liuliang if liuliang else 0
    jiaoyie = df['交易额'].apply(str2number).sum()
    huafei = df['花费'].apply(str2number).sum()
    touchan = jiaoyie / huafei if huafei else 0
    xiaoliang = chengjiaobishu
    chengjiaoe = jiaoyie
    return {
        "chengjiaobishu": convert2normal(chengjiaobishu),
        "baoguangliang": convert2normal(baoguangliang),
        "dianjiliang": convert2normal(liuliang),
        "liuliang": convert2normal(liuliang),
        "dianjilv": convert2normal(dianjilv),
        "zhuanhua": convert2normal(zhuanhua),
        "touchan": convert2normal(touchan),
        "xiaoliang": convert2normal(xiaoliang),
        "chengjiaoe": convert2normal(chengjiaoe),
        "huafei": convert2normal(huafei),
    }


def db_fetch_ads_of_id(good_id: str, target_date: datetime):
    df = pd.DataFrame(coll_ad.find({KEY_AD_ID: good_id, "target_date": target_date})).groupby('source').apply(
        get_ad_info)
    all_liuliang = df['多多搜索']['liuliang'] + df['多多场景']['liuliang'] + df['放心推']['liuliang']
    all_baoguangliang = df['多多搜索']['baoguangliang'] + df['多多场景']['baoguangliang'] + df['放心推']['baoguangliang']
    all_dianjiliang = df['多多搜索']['dianjiliang'] + df['多多场景']['dianjiliang'] + df['放心推']['dianjiliang']
    all_dianjilv = convert2normal(all_dianjiliang / all_baoguangliang)
    all_chengjiaobishu = df['多多搜索']['chengjiaobishu'] + df['多多场景']['chengjiaobishu'] + df['放心推']['chengjiaobishu']
    all_zhuanhua = convert2normal(all_chengjiaobishu / all_dianjiliang)
    all_xiaoliang = df['多多搜索']['xiaoliang'] + df['多多场景']['xiaoliang'] + df['放心推']['xiaoliang']
    all_chengjiaoe = df['多多搜索']['chengjiaoe'] + df['多多场景']['chengjiaoe'] + df['放心推']['chengjiaoe']
    all_huafei = df['多多搜索']['huafei'] + df['多多场景']['huafei'] + df['放心推']['huafei']
    all_touchan = convert2normal(all_chengjiaoe / all_huafei)
    data = {
        'date': target_date,
        'ddss_liuliang': df['多多搜索']['liuliang'],
        'ddss_dianjilv': df['多多搜索']['dianjilv'],
        'ddss_zhuanhua': df['多多搜索']['zhuanhua'],
        'ddss_touchan': df['多多搜索']['touchan'],
        'ddss_xiaoliang': df['多多搜索']['xiaoliang'],
        'ddss_chengjiaoe': df['多多搜索']['chengjiaoe'],
        'ddss_huafei': df['多多搜索']['huafei'],
        'ddcj_liuliang': df['多多场景']['liuliang'],
        'ddcj_dianjilv': df['多多场景']['dianjilv'],
        'ddcj_zhuanhua': df['多多场景']['zhuanhua'],
        'ddcj_touchan': df['多多场景']['touchan'],
        'ddcj_xiaoliang': df['多多场景']['xiaoliang'],
        'ddcj_chengjiaoe': df['多多场景']['chengjiaoe'],
        'ddcj_huafei': df['多多场景']['huafei'],
        'fxt_liuliang': df['放心推']['liuliang'],
        'fxt_dianjilv': df['放心推']['dianjilv'],
        'fxt_zhuanhua': df['放心推']['zhuanhua'],
        'fxt_touchan': df['放心推']['touchan'],
        'fxt_xiaoliang': df['放心推']['xiaoliang'],
        'fxt_chengjiaoe': df['放心推']['chengjiaoe'],
        'fxt_huafei': df['放心推']['huafei'],
        "all_liuliang": all_liuliang,
        "all_dianjilv": all_dianjilv,
        "all_zhuanhua": all_zhuanhua,
        "all_touchan": all_touchan,
        "all_xiaoliang": all_xiaoliang,
        "all_chengjiaoe": all_chengjiaoe,
        "all_huafei": all_huafei
    }

    return data


if __name__ == '__main__':
    data = db_fetch_ads_of_id('221058511472', datetime(2021, 4, 25))

