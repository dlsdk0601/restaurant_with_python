from stringcase import camelcase

from was import application


def generate():
    print('// GENERATED CODE - DO NOT MODIFY BY HAND')
    print('// coverage:ignore-file')
    print('// ignore_for_file: constant_identifier_names, unused_import')
    print("import './schema.gen.dart';")
    print("import './base.dart';")

    print('class Api extends ApiBase {')
    print('  Api(super.server);')

    for schema in application.api.app.export_api_schema():
        paths = ','.join(f"'{x}'" for x in schema.url.removeprefix('/').split('/'))
        print(f"""
            Future<{schema.res_data.__name__}?> {camelcase(schema.endpoint)}({schema.req.__name__} req) => 
                call([{paths}], req, {schema.res_data.__name__}.fromJson);
        """)

    print('}')


if __name__ == '__main__':
    generate()
