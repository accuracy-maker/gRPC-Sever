from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENERATED: _ClassVar[GenerationStatus]
    FAILED: _ClassVar[GenerationStatus]
GENERATED: GenerationStatus
FAILED: GenerationStatus

class InferenceRequest(_message.Message):
    __slots__ = ("prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    def __init__(self, prompt: _Optional[str] = ...) -> None: ...

class AudioResponse(_message.Message):
    __slots__ = ("audio", "sample_rate", "status")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    audio: bytes
    sample_rate: int
    status: GenerationStatus
    def __init__(self, audio: _Optional[bytes] = ..., sample_rate: _Optional[int] = ..., status: _Optional[_Union[GenerationStatus, str]] = ...) -> None: ...

class ImageRequest(_message.Message):
    __slots__ = ("prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    def __init__(self, prompt: _Optional[str] = ...) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ("image", "width", "height", "format", "status")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    width: int
    height: int
    format: str
    status: GenerationStatus
    def __init__(self, image: _Optional[bytes] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., format: _Optional[str] = ..., status: _Optional[_Union[GenerationStatus, str]] = ...) -> None: ...
