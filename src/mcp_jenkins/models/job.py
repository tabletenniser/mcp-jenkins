from typing import Union

from pydantic import BaseModel, Field


class JobBase(BaseModel):
    class_: str = Field(..., alias='_class')
    name: str
    url: str
    fullname: str

    class Config:
        validate_by_name = True


class Job(JobBase):
    color: str


class Folder(JobBase):
    jobs: list[Union['Job', 'Folder']]
