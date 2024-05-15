import 'package:flutter/cupertino.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:restaurant_app/model/storage.dart';

import '../main.dart';

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
    // final re = await api.userAccessTokenValidate(const UserAccessTokenValidateReq());
    // final user = re?.user;
    // if (user == null) {
    //   accessToken = null;
    //   notifyListeners();
    //   return;
    // }
    //
    // userInfo = UserInfo(user.pk, user.name);
    //
    // notifyListeners();
  }
}

final userModel = UserModel();

@freezed
class UserInfo with _$UserInfo {
  // TODO :: user show 에 따라 바꿀 것.
  factory UserInfo(int pk, String name) = _UserInfo;
}
