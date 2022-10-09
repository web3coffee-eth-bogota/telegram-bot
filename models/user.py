from datetime import datetime

from peewee import BigIntegerField, CharField, BooleanField, DateTimeField

from .base import BaseModel, database


class User(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = CharField()
    language = CharField(default='en')
    social_link = CharField(default='')
    career = CharField(default='')
    interests = CharField(default='')
    location = CharField(default='')

    is_admin = BooleanField(default=False)

    created_at = DateTimeField(default=lambda: datetime.utcnow())

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    class Meta:
        table_name = 'users'
