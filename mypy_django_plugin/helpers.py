import typing
from typing import Dict, Optional, NamedTuple

from mypy.nodes import Expression, StrExpr, MypyFile, TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import Type, UnionType, NoneTyp

MODEL_CLASS_FULLNAME = 'django.db.models.base.Model'
QUERYSET_CLASS_FULLNAME = 'django.db.models.query.QuerySet'
FOREIGN_KEY_FULLNAME = 'django.db.models.fields.related.ForeignKey'
ONETOONE_FIELD_FULLNAME = 'django.db.models.fields.related.OneToOneField'
DUMMY_SETTINGS_BASE_CLASS = 'django.conf._DjangoConfLazyObject'

Argument = NamedTuple('Argument', fields=[
    ('arg', Expression),
    ('arg_type', Type)
])


def get_call_signature_or_none(ctx: FunctionContext) -> Optional[Dict[str, Argument]]:
    result: Dict[str, Argument] = {}
    positional_args_only = []
    positional_arg_types_only = []
    for arg, arg_name, arg_type in zip(ctx.args, ctx.arg_names, ctx.arg_types):
        if arg_name is None:
            positional_args_only.append(arg)
            positional_arg_types_only.append(arg_type)
            continue

        if len(arg) == 0 or len(arg_type) == 0:
            continue

        result[arg_name] = (arg[0], arg_type[0])

    callee = ctx.context.callee
    if '__init__' not in callee.node.names:
        return None

    init_type = callee.node.names['__init__'].type
    arg_names = init_type.arg_names[1:]
    for arg, arg_name, arg_type in zip(positional_args_only,
                                       arg_names[:len(positional_args_only)],
                                       positional_arg_types_only):
        result[arg_name] = (arg[0], arg_type[0])

    return result


def make_optional(typ: Type) -> Type:
    return UnionType.make_simplified_union([typ, NoneTyp()])


def make_required(typ: Type) -> Type:
    if not isinstance(typ, UnionType):
        return typ
    items = [item for item in typ.items if not isinstance(item, NoneTyp)]
    return UnionType.make_union(items)


def get_obj_type_name(typ: typing.Type) -> str:
    return typ.__module__ + '.' + typ.__qualname__


def get_models_file(app_name: str, all_modules: typing.Dict[str, MypyFile]) -> Optional[MypyFile]:
    models_module = '.'.join([app_name, 'models'])
    return all_modules.get(models_module)


def get_model_type_from_string(expr: StrExpr,
                               all_modules: Dict[str, MypyFile]) -> Optional[TypeInfo]:
    app_name, model_name = expr.value.split('.')

    models_file = get_models_file(app_name, all_modules)
    if models_file is None:
        # not imported so far, not supported
        return None
    sym = models_file.names.get(model_name)
    if not sym or not isinstance(sym.node, TypeInfo):
        # no such model found in the app / node is not a class definition
        return None
    return sym.node
