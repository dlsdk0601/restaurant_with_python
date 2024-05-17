import os

from flask import url_for
from more_itertools import flatten
from stringcase import camelcase

from ex.py.datetime_ex import now
from was import blueprints
from was.application import app


def main() -> None:
    print('/* tslint:disable */')
    print('/* eslint-disable */')
    print(f'// 자동생성 파일 수정 금지 - {os.path.basename(__file__)} {now()}')
    print('')

    schemas = blueprints.app.export_api_schema()

    # 연결된 모든 스키마 임포트
    schema_names = sorted(set(flatten([i.req.__name__, i.res_data.__name__] for i in schemas)))
    print(f"import {'{' + ','.join(schema_names) + '}'} from './schema.g';")
    # Base 클래스 임포트
    print("import {ApiBase} from './apiBase';")
    print('')

    # 클래스 정의
    print(f'export class Api extends ApiBase {{')
    for schema in schemas:
        url = url_for(blueprints.app.name + '.' + schema.endpoint)
        print(
            f"\treadonly {camelcase(schema.endpoint)} = "
            f"this.c<{schema.req.__name__}, {schema.res_data.__name__}>('{url}');"
        )
    print('}')


if __name__ == '__main__':
    with app.test_request_context():
        main()
