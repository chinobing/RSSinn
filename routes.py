from fastapi import APIRouter
from pages import index, status, sitemap
from feeds import toscrape, bridgewater, chinastarmarket, esnai, kr, xl720, tenjqka, yyets, csrc

router = APIRouter()
"""RSSINN|Routes"""
router.include_router(index)
router.include_router(status)
router.include_router(sitemap)

"""金融|Finance"""
router.include_router(csrc, prefix='/csrc', tags = ['金融|Finance"'])

"""媒体|Media"""
router.include_router(bridgewater, prefix='/bridgewater', tags = ['媒体 | Media'])

"""论坛|Forum"""
router.include_router(esnai, prefix='/esnai', tags = ['论坛 | Forum'])

"""新闻|News"""
router.include_router(kr, prefix='/36kr', tags = ['新闻 | News'])
router.include_router(chinastarmarket, prefix='/chinastarmarket', tags = ['新闻 | News'])
router.include_router(tenjqka, prefix='/10jqka', tags = ['新闻 | News'])

"""娱乐|Entertainment"""
router.include_router(xl720, prefix='/xl720', tags = ['媒体 | Entertainment'])
router.include_router(yyets, prefix='/yyets', tags = ['媒体 | Entertainment'])

"""DEMO"""
router.include_router(toscrape, prefix='/toscrape', tags = ['DEMO'])