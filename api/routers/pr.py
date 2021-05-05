from fastapi import APIRouter

api_pr = APIRouter(prefix='/pr', tags=['反馈'])


@api_pr.post('/help', summary='问题求助')
def pr_help():
    return ''


@api_pr.post('/advice', summary='建议吐槽')
def pr_advice():
    return ''
