
from fastapi_rss import RSSFeed, RSSResponse, Item



"""
class Item(BaseModel):
    title: str
    link: Optional[str]
    description: Optional[str]
    author: Optional[str]
    category: Optional[Category]
    comments: Optional[str]
    enclosure: Optional[Enclosure]
    guid: Optional[GUID]
    pub_date: Optional[datetime.datetime]
    source: Optional[Source]
"""


docker build -t "rssinn" .

docker run -it --rm -p 28085:28085 rssinn