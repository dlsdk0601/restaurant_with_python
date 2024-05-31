import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:restaurant_app/model/user.dart';
import 'package:restaurant_app/router.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    if (userModel.accessToken == null) {
      context.go(const SignInRoute().location);
      return Container();
    }

    return Center(
      child: ElevatedButton(
        onPressed: () {
          userModel.signOut();
        },
        child: const Text("로그 아웃"),
      ),
    );
  }
}
