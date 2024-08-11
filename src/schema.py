from pydantic import BaseModel

from .constants import PAGE_ID_URL


class Post(BaseModel):
    id: str
    content: str
    posted_at: str
    page: str

    @property
    def url(self) -> str:
        return PAGE_ID_URL.format(id=self.id, page=self.page)
