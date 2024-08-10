from pydantic import BaseModel


class Post(BaseModel):
    id: str
    content: str
    posted_at: str
