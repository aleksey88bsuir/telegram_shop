from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User


class Post(Base, UserRelationMixin):
    _user_back_populates = "posts"
    title: Mapped[str] = mapped_column(String(50), unique=False)
    body: Mapped[str] = mapped_column(Text,
                                      default='',
                                      server_default=''
                                      )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r})"

    def __repr__(self):
        return str(self)
