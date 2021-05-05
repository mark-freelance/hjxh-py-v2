from enum import Enum

from api.models.base import MongoModel


class AccountCategory(Enum):
	DDBK = "多多情报"  # 多多情报
	DDCM = "多多参谋"  # 多多参谋


class AccountStatus(Enum):
	Verified = "已验证"
	NotVerified = "待验证"
	FailForVerification = "验证失败"
	FailForInactive = "已过期"


class Account(MongoModel):
	username: str
	password: str
	category: AccountCategory
	status: AccountStatus = AccountStatus.NotVerified
	created_time: int
	note: str
