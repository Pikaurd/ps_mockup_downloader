import datetime
import logging
from peewee import *

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# __db_path__ = 'mockup_downloader.sqlite3'
__db_path__ = ':memory:'
db = SqliteDatabase(':memory:')


def setup():
    db.connect()
    db.create_tables([MockupEntity])


class BaseModel(Model):
    class Meta:
        database = db


class MockupEntity(BaseModel):
    title = TextField()
    description = TextField()
    cover_url = TextField()  # 封面图路径
    filename = TextField()
    source = TextField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<MockupEntity (id={self.id}, title={self.title})>'
