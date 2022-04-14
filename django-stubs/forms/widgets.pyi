import datetime
import sys
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, Union

from django.core.files.base import File
from django.db.models.fields import _FieldChoices
from django.forms.renderers import BaseRenderer
from django.forms.utils import _DataT, _FilesT
from django.utils.datastructures import _ListOrTuple
from django.utils.functional import _Getter
from django.utils.safestring import SafeString
from typing_extensions import Literal

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

_OptAttrs = Dict[str, Any]

class MediaOrderConflictWarning(RuntimeWarning): ...

class Media:
    def __init__(
        self,
        media: Optional[type] = ...,
        css: Optional[Dict[str, Sequence[str]]] = ...,
        js: Optional[Sequence[str]] = ...,
    ) -> None: ...
    def render(self) -> SafeString: ...
    def render_js(self) -> List[SafeString]: ...
    def render_css(self) -> Iterable[SafeString]: ...
    def absolute_path(self, path: str) -> str: ...
    def __getitem__(self, name: str) -> Media: ...
    @staticmethod
    def merge(*lists: Iterable[Any]) -> List[Any]: ...
    def __add__(self, other: Media) -> Media: ...

class MediaDefiningClass(type): ...

class Widget(metaclass=MediaDefiningClass):
    needs_multipart_form: bool = ...
    is_localized: bool = ...
    is_required: bool = ...
    supports_microseconds: bool = ...
    attrs: _OptAttrs = ...
    template_name: str
    media: _Getter[Media]
    def __init__(self, attrs: Optional[_OptAttrs] = ...) -> None: ...
    @property
    def is_hidden(self) -> bool: ...
    def subwidgets(self, name: str, value: Any, attrs: _OptAttrs = ...) -> Iterator[Dict[str, Any]]: ...
    def format_value(self, value: Any) -> Optional[str]: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def render(
        self, name: str, value: Any, attrs: Optional[_OptAttrs] = ..., renderer: Optional[BaseRenderer] = ...
    ) -> SafeString: ...
    def build_attrs(self, base_attrs: _OptAttrs, extra_attrs: Optional[_OptAttrs] = ...) -> Dict[str, Any]: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
    def id_for_label(self, id_: str) -> str: ...
    def use_required_attribute(self, initial: Any) -> bool: ...

class Input(Widget):
    input_type: str = ...
    template_name: str = ...

class TextInput(Input):
    input_type: str = ...
    template_name: str = ...

class NumberInput(Input):
    input_type: str = ...
    template_name: str = ...

class EmailInput(Input):
    input_type: str = ...
    template_name: str = ...

class URLInput(Input):
    input_type: str = ...
    template_name: str = ...

class PasswordInput(Input):
    render_value: bool = ...
    input_type: str = ...
    template_name: str = ...
    def __init__(self, attrs: Optional[_OptAttrs] = ..., render_value: bool = ...) -> None: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...

class HiddenInput(Input):
    choices: _FieldChoices
    input_type: str = ...
    template_name: str = ...

class MultipleHiddenInput(HiddenInput):
    template_name: str = ...

class FileInput(Input):
    input_type: str = ...
    template_name: str = ...
    needs_multipart_form: bool = ...
    def format_value(self, value: Any) -> None: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
    def use_required_attribute(self, initial: Any) -> bool: ...

FILE_INPUT_CONTRADICTION: object

class ClearableFileInput(FileInput):
    clear_checkbox_label: str = ...
    initial_text: str = ...
    input_text: str = ...
    template_name: str = ...
    def clear_checkbox_name(self, name: str) -> str: ...
    def clear_checkbox_id(self, name: str) -> str: ...
    def is_initial(self, value: Optional[Union[File, str]]) -> bool: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...

class Textarea(Widget):
    template_name: str = ...
    def __init__(self, attrs: Optional[_OptAttrs] = ...) -> None: ...

class DateTimeBaseInput(TextInput):
    format_key: str = ...
    format: Optional[str] = ...
    supports_microseconds: bool = ...
    def __init__(self, attrs: Optional[_OptAttrs] = ..., format: Optional[str] = ...): ...

class DateInput(DateTimeBaseInput):
    format_key: str = ...
    template_name: str = ...

class DateTimeInput(DateTimeBaseInput):
    format_key: str = ...
    template_name: str = ...

class TimeInput(DateTimeBaseInput):
    format_key: str = ...
    template_name: str = ...

def boolean_check(v: Any) -> bool: ...

class _CheckCallable(Protocol):
    def __call__(self, __value: Any) -> bool: ...

class CheckboxInput(Input):
    check_test: _CheckCallable = ...
    input_type: str = ...
    template_name: str = ...
    def __init__(self, attrs: Optional[_OptAttrs] = ..., check_test: Optional[_CheckCallable] = ...) -> None: ...

class ChoiceWidget(Widget):
    allow_multiple_selected: bool = ...
    input_type: Optional[str] = ...
    template_name: str = ...
    option_template_name: Optional[str] = ...
    add_id_index: bool = ...
    checked_attribute: Any = ...
    option_inherits_attrs: bool = ...
    choices: _FieldChoices = ...
    def __init__(self, attrs: Optional[_OptAttrs] = ..., choices: _FieldChoices = ...) -> None: ...
    def subwidgets(self, name: str, value: Any, attrs: _OptAttrs = ...) -> Iterator[Dict[str, Any]]: ...
    def options(self, name: str, value: List[str], attrs: Optional[_OptAttrs] = ...) -> Iterator[Dict[str, Any]]: ...
    def optgroups(
        self, name: str, value: List[str], attrs: Optional[_OptAttrs] = ...
    ) -> List[Tuple[Optional[str], List[Dict[str, Any]], Optional[int]]]: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def create_option(
        self,
        name: str,
        value: Any,
        label: Union[int, str],
        selected: bool,
        index: int,
        subindex: Optional[int] = ...,
        attrs: Optional[_OptAttrs] = ...,
    ) -> Dict[str, Any]: ...
    def id_for_label(self, id_: str, index: str = ...) -> str: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def format_value(self, value: Any) -> List[str]: ...  # type: ignore

class Select(ChoiceWidget):
    input_type: Optional[str] = ...
    template_name: str = ...
    option_template_name: str = ...
    add_id_index: bool = ...
    checked_attribute: Any = ...
    option_inherits_attrs: bool = ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def use_required_attribute(self, initial: Any) -> bool: ...

class NullBooleanSelect(Select):
    def __init__(self, attrs: Optional[_OptAttrs] = ...) -> None: ...
    def format_value(self, value: Any) -> str: ...  # type: ignore
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Optional[bool]: ...

class SelectMultiple(Select):
    allow_multiple_selected: bool = ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...

class RadioSelect(ChoiceWidget):
    can_add_related: bool
    input_type: str = ...
    template_name: str = ...
    option_template_name: str = ...

class CheckboxSelectMultiple(ChoiceWidget):
    can_add_related: bool
    input_type: str = ...
    template_name: str = ...
    option_template_name: str = ...
    def use_required_attribute(self, initial: Any) -> bool: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
    def id_for_label(self, id_: str, index: Optional[str] = ...) -> str: ...

class MultiWidget(Widget):
    template_name: str = ...
    widgets: Sequence[Widget] = ...
    def __init__(
        self,
        widgets: Union[Dict[str, Union[Widget, Type[Widget]]], Sequence[Union[Widget, Type[Widget]]]],
        attrs: Optional[_OptAttrs] = ...,
    ) -> None: ...
    @property
    def is_hidden(self) -> bool: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def id_for_label(self, id_: str) -> str: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> List[Any]: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
    def decompress(self, value: Any) -> Optional[Any]: ...
    media: _Getter[Media] = ...
    @property
    def needs_multipart_form(self) -> bool: ...  # type: ignore

class SplitDateTimeWidget(MultiWidget):
    supports_microseconds: bool = ...
    template_name: str = ...
    widgets: Tuple[DateInput, TimeInput]
    def __init__(
        self,
        attrs: Optional[_OptAttrs] = ...,
        date_format: Optional[str] = ...,
        time_format: Optional[str] = ...,
        date_attrs: Optional[Dict[str, str]] = ...,
        time_attrs: Optional[Dict[str, str]] = ...,
    ) -> None: ...
    def decompress(self, value: Any) -> Tuple[Optional[datetime.date], Optional[datetime.time]]: ...

class SplitHiddenDateTimeWidget(SplitDateTimeWidget):
    template_name: str = ...
    def __init__(
        self,
        attrs: Optional[_OptAttrs] = ...,
        date_format: Optional[str] = ...,
        time_format: Optional[str] = ...,
        date_attrs: Optional[Dict[str, str]] = ...,
        time_attrs: Optional[Dict[str, str]] = ...,
    ) -> None: ...

class SelectDateWidget(Widget):
    none_value: Tuple[Literal[""], str] = ...
    month_field: str = ...
    day_field: str = ...
    year_field: str = ...
    template_name: str = ...
    input_type: str = ...
    select_widget: Type[ChoiceWidget] = ...
    date_re: Any = ...
    years: Iterable[Union[int, str]] = ...
    months: Mapping[int, str] = ...
    year_none_value: Tuple[Literal[""], str] = ...
    month_none_value: Tuple[Literal[""], str] = ...
    day_none_value: Tuple[Literal[""], str] = ...
    def __init__(
        self,
        attrs: Optional[_OptAttrs] = ...,
        years: Optional[Iterable[Union[int, str]]] = ...,
        months: Optional[Mapping[int, str]] = ...,
        empty_label: Optional[Union[str, _ListOrTuple[str]]] = ...,
    ) -> None: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs]) -> Dict[str, Any]: ...
    def format_value(self, value: Any) -> Dict[str, Union[str, int, None]]: ...  # type: ignore
    def id_for_label(self, id_: str) -> str: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Union[str, None, Any]: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
