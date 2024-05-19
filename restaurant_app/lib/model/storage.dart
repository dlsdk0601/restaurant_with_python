import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class Storage {
  Storage._();

  final _secureStorage = const FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
      resetOnError: true,
    ),
  );

  Future<void> writeAccessToken(String? accessToken) async {
    await _secureStorage.write(key: _keyAccessToken, value: accessToken);
  }

  Future<String?> readAccessToken() {
    return _secureStorage.read(key: _keyAccessToken);
  }

  static const _keyAccessToken = 'access-token';
}

final storage = Storage._();
