import json
from typing import Any, Callable, Literal

from pydantic import BaseModel, Field
from pydantic.main import IncEx


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
    jobs: list[JobBase]

    def model_dump(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx | None = None,
            exclude: IncEx | None = None,
            context: Any | None = None,
            by_alias: bool | None = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool | Literal['none', 'warn', 'error'] = True,
            fallback: Callable[[Any], Any] | None = None,
            serialize_as_any: bool = False
    ) -> dict[str, Any]:
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any
        )
        data.update({'jobs': [job.model_dump(mode=mode, by_alias=by_alias) for job in self.jobs]})
        return data

    def model_dump_json(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx | None = None,
            exclude: IncEx | None = None,
            context: Any | None = None,
            by_alias: bool | None = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool | Literal['none', 'warn', 'error'] = True,
            fallback: Callable[[Any], Any] | None = None,
            serialize_as_any: bool = False
    ) -> str:
        data = self.model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any
        )
        return json.dumps(data, indent=4, ensure_ascii=False)
