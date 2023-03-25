from datetime import datetime
from typing import Optional, List, Union
from uuid import uuid4

from .entity import Entity
from .event_metadata import EventMetadata
from pydantic import BaseModel, root_validator
from typing import Tuple

from .value_object.operation import RecordFlag
from .value_object.storage_info import StorageInfo


class Tags(BaseModel):
    values: Tuple['str', ...] = ()
    count: int = 0

    class Config:
        validate_assignment = True

    @root_validator
    def total_tags(cls, values):
        values["count"] = len(values.get("values"))
        return values

    def add(self, tag: Union[str, List[str]]):

        if isinstance(tag, list):
            tag = tuple(tag)
            self.values += tag
        else:
            self.values += tag,

        self.count = len(self.values)


class Browser(BaseModel):
    family: Optional[str] = None
    version: Optional[str] = None


class OS(BaseModel):
    family: Optional[str] = None
    version: Optional[str] = None


class Device(BaseModel):
    family: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None


class UserAgent(BaseModel):
    bot: Optional[bool] = False
    browser: Optional[Browser] = Browser()
    os: Optional[OS] = OS()
    device: Optional[Device] = Device()


class EventSession(Entity):
    start: datetime = datetime.utcnow()
    duration: float = 0
    tz: Optional[str] = 'utc'
    agent: Optional[UserAgent] = UserAgent()


class Event(Entity):
    metadata: EventMetadata
    type: str
    properties: Optional[dict] = {}
    traits: Optional[dict] = {}
    operation: RecordFlag = RecordFlag()

    source: Entity
    session: Optional[EventSession] = None
    profile: Optional[Entity] = None
    context: Optional[dict] = {}
    request: Optional[dict] = {}
    config: Optional[dict] = {}
    tags: Tags = Tags()
    aux: dict = {}

    def replace(self, event):
        if isinstance(event, Event):
            self.id = event.id
            self.metadata = event.metadata
            self.type = event.type
            self.properties = event.properties
            self.traits = event.traits
            # do not replace those - read only
            # self.source = event.source
            # self.session = event.session
            # self.profile = event.profile
            self.context = event.context
            self.request = event.request
            self.config = event.config
            self.tags = event.tags
            self.aux = event.aux

    def get_ip(self):
        if 'headers' in self.request and 'x-forwarded-for' in self.request['headers']:
            return self.request['headers']['x-forwarded-for']
        return None

    def is_persistent(self) -> bool:
        if 'save' in self.config and isinstance(self.config['save'], bool):
            return self.config['save']
        else:
            return True

    @staticmethod
    def new(data: dict) -> 'Event':
        data['id'] = str(uuid4())
        return Event(**data)

    @staticmethod
    def storage_info() -> StorageInfo:
        return StorageInfo(
            'event',
            Event,
            multi=True
        )
