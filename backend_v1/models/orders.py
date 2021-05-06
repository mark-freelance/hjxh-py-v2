from pydantic import BaseModel
from typing import Any


class Order(BaseModel):
    """
    todo: 需要对这些Any状态做细化
    """
    after_sales_id: Any = None
    after_sales_status: Any = None
    biz_type: int = None
    business_intra_sales: bool = None
    buyer_memo: str = None
    city_name: str = None
    confirm_time: int = None
    created_at: int = None
    delivery_one_day: Any = None
    district_name: str = None
    duoduo_wholesale: bool = None
    extraGoodsList: Any = None
    good_ware_internal_buy: bool = None
    goods_amount: int = None
    goods_id: int = None
    goods_name: str = None
    goods_number: int = None
    group_status: int = None
    hasExtraGoods: bool = None
    is_exist_fine_info: int = None
    is_ota_virtual_card: bool = None
    is_oversea_without_idcard_info: bool = None
    mall_remark: Any = None
    mall_remark_name: Any = None
    mall_remark_tag: Any = None
    merchant_discount: Any = None
    nickname: str = None
    no_need_ship: bool = None
    no_trace_delivery: bool = None
    order_amount: int = None
    order_handle_status: Any = None
    order_sn: str = None
    order_status: int = None
    order_status_str: str = None
    order_time: int = None
    out_sku_sn: str = None
    pay_status: int = None
    payment_start_time: int = None
    platform_discount: int = None
    promise_shipping_time: int = None
    province_name: str = None
    receive_name: str = None
    remark_status: int = None
    risk_status: int = None
    self_contained: Any = None
    shipping_amount: int = None
    shipping_id: int = None
    shipping_status: int = None
    shipping_time: int = None
    spec: str = None
    step_pay_orders: Any = None
    stockout_source_type: Any = None
    thumb_url: str = None
    trade_type: int = None
    type: int = None
    urge_shipping_time: Any = None