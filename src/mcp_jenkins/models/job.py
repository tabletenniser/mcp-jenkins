from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True
    )

    class_: str = Field(..., alias='_class')
    name: str
    url: str
    fullname: str


class Job(JobBase):
    color: str


class Folder(JobBase):
    jobs: list[Union['Job', 'Folder']]
