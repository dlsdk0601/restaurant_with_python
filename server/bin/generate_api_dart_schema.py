import datetime
import re
from enum import Enum
from typing import Type, get_origin, Any, TypeVar, Tuple, get_args, TypeGuard
from uuid import UUID

from more_itertools import flatten
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.schema import get_flat_models_from_models
from stringcase import camelcase

from ex.api import ResStatus, GenericModel
from ex.sqlalchemy_ex import Pagination, PageRow
from was import application


def generate() -> None:
    print('// GENERATED CODE - DO NOT MODIFY BY HAND')
    print('// coverage:ignore-file')
    print('// ignore_for_file: constant_identifier_names, unused_import')

    print("import 'package:freezed_annotation/freezed_annotation.dart';")
    print("import './pagination.dart';")
    print("part 'schema.gen.freezed.dart';")
    print("part 'schema.gen.g.dart';")
    print("""
        @freezed
        class Res with _$Res {
          const factory Res({
            required List<String> errors,
            required List<dynamic> validationErrors,
            required ResStatus status,
          }) = _Res;

          factory Res.fromJson(Map<String, Object?> json) => _$ResFromJson(json);
        }
    """)

    api_schemas = list(flatten([i.req, i.res_data] for i in application.blueprints.app.export_api_schema()))
    models: set[Type[BaseModel | Enum | GenericModel]] = get_flat_models_from_models(api_schemas)
    models.add(ResStatus)
    for model in sorted(models, key=lambda x: x.__name__):
        if issubclass(model, Enum):
            print(generate_enum(model))
        elif issubclass(model, Pagination):
            print(generate_pagination_converter(model))
        elif issubclass(model, PageRow):
            # freezed 와 json_serialize 가 지원하지 못한다.
            continue
        else:
            print(generate_class(model))


def generate_class(model: Type[BaseModel]) -> str:
    # (name, extends) = _de_generic_name(model.__name__)
    name = model.__name__
    properties: list[str] = []
    field: ModelField
    for field in model.__fields__.values():
        annotation, type_ = _field_dart_type(field.outer_type_, field.type_, bool(field.required))
        if field.required:
            type_ = 'required ' + type_
        if annotation:
            type_ = annotation + ' ' + type_
        properties.append(f'{type_} {camelcase(field.name)}')
    constructor_args = ''
    if properties:
        constructor_args = '{' + ', '.join(properties) + '}'
    # if not extends:
    #     extends = ''
    # else:
    #     extends = ' extends ' + extends

    base_args = list(flatten(map(get_args, getattr(model, '__orig_bases__', []))))
    if base_args:
        base_type_vars = filter(lambda x: isinstance(x, TypeVar), base_args)
        base_type_names = map(lambda x: x.__name__, base_type_vars)
        model_type_variables = '<' + ', '.join(base_type_names) + '>'
    else:
        model_type_variables = ''
    return f"""
    @freezed
    class {name}{model_type_variables} with _${name} implements ToJson {{
      const factory {name}({constructor_args}) = _{name};

      factory {name}.fromJson(Map<String, Object?> json) => _${name}FromJson(json);
    }}
    """


def generate_pagination_converter(model: Type[Pagination]) -> str:
    (type_name, item_type_name) = _parse_pagination_name(model)
    name = _build_pagination_converter_name(type_name, item_type_name)

    return f'''
    class {name}
        extends JsonConverter<
            Pagination<List<PageRow<{item_type_name}>>>, 
            Map<String, Object?>
        > 
        with PaginationConverter<{item_type_name}> {{
        const {name}();
        
        @override
        {item_type_name} Function(Map<String, Object?> json) getFromJson() {{
            return {item_type_name}.fromJson;
        }}
    }}
    '''


def _parse_pagination_name(model: Type[Pagination]) -> Tuple[str, str]:
    # OPT :: Generic Type Inspection 이 불가능하다.
    match = re.match(r'^(Pagination)\[([^]]+)]$', model.__name__)
    assert match, f'이름은 반드시 Pagination[?] 형태 여야 한다 : model.__name__={model.__name__}'
    return match.group(1), match.group(2)


def _build_pagination_converter_name(type_name: str, row_item_type_name: str) -> str:
    return '_' + type_name + row_item_type_name + 'Converter'


def _field_dart_type(outer_type: Any, field_type: Any, required: bool) -> Tuple[str | None, str]:
    origin_type = get_origin(outer_type)
    annotation: str | None = None
    if outer_type is str or outer_type is UUID:
        type_ = 'String'
    elif outer_type is int:
        type_ = 'int'
    elif outer_type is float:
        type_ = 'double'
    elif outer_type is bool:
        type_ = 'bool'
    elif outer_type is datetime.datetime:
        type_ = 'DateTime'
    elif outer_type is bytes:
        type_ = 'String'
    elif _safe_issubclass(outer_type, Enum):
        type_ = outer_type.__name__
    elif _safe_issubclass(outer_type, Pagination):
        (type_name, page_row_type_name) = _parse_pagination_name(outer_type)
        type_ = f'{type_name}<List<PageRow<{page_row_type_name}>>>'
        annotation = f'@{_build_pagination_converter_name(type_name, page_row_type_name)}()'
    elif getattr(outer_type, 'Config', None) is not None:
        # Model 타입
        type_ = outer_type.__name__
    elif origin_type is list:
        def filter_valids(value: str | None) -> TypeGuard[str]:
            return value is not None

        list_item_type = ' '.join(filter(filter_valids, _field_dart_type(field_type, field_type, required)))
        type_ = f'List<{list_item_type}>'
    elif isinstance(outer_type, TypeVar):
        # generic 일경우 그냥 출력해 준다.
        type_ = outer_type.__name__
    else:
        raise NotImplementedError(
            f'TODO :: 나머지 타입 처리 : '
            f'{outer_type=}, {field_type=}, {origin_type=}'
        )
    if not required:
        type_ += '?'
    return annotation, type_


def generate_enum(model: Type[Enum]) -> str:
    return f"""
        enum {model.__name__} {{ {', '.join(model)} }}
    """


def _safe_issubclass(cls: type, *parents: type) -> bool:
    try:
        return issubclass(cls, parents)
    except TypeError:
        return False


# def _de_generic_name(name: str) -> Tuple[str, str | None]:
#     if matched := re.match(r'([^ \[\]]+)\[([^]]+)', name):
#         return matched.group(1) + matched.group(2), \
#                matched.group(1) + '<' + matched.group(2) + '>'
#     return name, None
#

if __name__ == '__main__':
    generate()
