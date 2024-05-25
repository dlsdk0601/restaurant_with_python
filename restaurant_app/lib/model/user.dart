import 'package:flutter/cupertino.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:restaurant_app/api/schema.gen.dart';
import 'package:restaurant_app/model/storage.dart';

import '../globals.dart';

part 'user.freezed.dart';

class UserModel extends ChangeNotifier {
  String? accessToken;
  UserInfo? userInfo;

  Future<void> init() async {
    accessToken = await storage.readAccessToken();

    if (accessToken == null) {
      return;
    }

    await validateAccessToken();
    if (accessToken == null) {
      // 만약 Validation 에 실패하였으면 이건 사용불 가능한 키
      storage.writeAccessToken(null);
    }

    // TODO :: 로그인 상태 변경 listener 추가
    // 로그인이 풀리면 로그인 페이지로 강제 이동
  }

  Future<void> validateAccessToken() async {
    final res = await api.userShow(const UserShowReq());

    if (res == null) {
      accessToken = null;
      notifyListeners();
      return;
    }

    userInfo = UserInfo(res.pk, res.email, res.name, res.image, res.cartCount);
    notifyListeners();
  }

  Future<void> signOut() async {}

  Future<void> setAccessToken(String accessToken) async {
    this.accessToken = accessToken;
    await validateAccessToken();
    await storage.writeAccessToken(this.accessToken);
  }
}

final userModel = UserModel();

@freezed
class UserInfo with _$UserInfo {
  factory UserInfo(
    int pk,
    String email,
    String name,
    Bsset bsset,
    int cartCount,
  ) = _UserInfo;
}
