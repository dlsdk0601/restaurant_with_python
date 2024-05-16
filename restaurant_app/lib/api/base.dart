import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:restaurant_app/api/pagination.dart';
import 'package:restaurant_app/api/schema.gen.dart';
import 'package:restaurant_app/config.dart';
import 'package:restaurant_app/model/user.dart';

import '../view/block.dart';

abstract class ApiBase {
  final _tag = 'ApiBase';
  final Uri _server;

  ApiBase(this._server);

  @protected
  Future<RESPONSE?> call<REQUEST extends ToJson, RESPONSE>(
    List<String> path,
    REQUEST req,
    RESPONSE Function(Map<String, Object?> json) resFromJson,
  ) {
    return _call(
      () => http.post(
        _buildUri(path),
        headers: _buildHeaders(),
        body: jsonEncode(req.toJson()),
      ),
      resFromJson,
    );
  }

  Uri _buildUri(List<String> path) {
    return Uri(
      scheme: _server.scheme,
      host: _server.host,
      port: _server.port,
      pathSegments: [..._server.pathSegments, ...path],
    );
  }

  @protected
  Future<RESPONSE?> _call<REQUEST extends ToJson, RESPONSE>(
    Future<http.Response> Function() req,
    RESPONSE Function(Map<String, Object?> json) resFromJson,
  ) {
    return block(() async {
      try {
        final response = await req();

        if (response.statusCode != 200) {
          logger.e([
            _tag,
            'request err : statusCode = ${response.statusCode}',
            response.body,
          ]);
          confirm('서버 오류 - response.statusCode = ${response.statusCode}');
          return null;
        }

        final json = jsonDecode(response.body) as Map<String, dynamic>;

        final res = Res.fromJson(json);

        switch (res.status) {
          case ResStatus.OK:
            break;
          case ResStatus.LOGIN_REQUIRED:
          case ResStatus.INVALID_ACCESS_TOKEN:
            await userModel.signOut();
            return null;
          case ResStatus.NO_PERMISSION:
            confirm('권한이 필요합니다.');
            return null;
          case ResStatus.NOT_FOUND:
            confirm('요청한 리소스를 찾을 수 없습니다.');
            return null;
        }

        if (res.errors.isNotEmpty) {
          confirm(res.errors.join("\n"));
          return null;
        }

        if (res.validationErrors.isNotEmpty) {
          confirm(jsonEncode(json['validationErrors']));
          return null;
        }

        return resFromJson(json['data']);
      } catch (error, stackTrace) {
        logger.e('api 오류', error: error, stackTrace: stackTrace);
        confirm(error.toString());
        return null;
      }
    });
  }

  Map<String, String> _buildHeaders() {
    final accessToken = userModel.accessToken;
    return {if (accessToken != null) 'X-Access-Token': accessToken};
  }
}

void confirm(String text) {
  // TODO :: confirm context 완성
  // throw Exception;
}
