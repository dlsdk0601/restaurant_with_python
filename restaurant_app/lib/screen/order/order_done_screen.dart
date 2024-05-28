import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/router.dart';
import 'package:restaurant_app/view/default_layout.dart';

class OrderDoneScreen extends StatelessWidget {
  const OrderDoneScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultLayout(
      title: "결제 완료",
      child: Padding(
        padding: const EdgeInsets.symmetric(
          horizontal: 16.0,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(
              Icons.thumb_up_alt_outlined,
              color: PRIMARY_COLOR,
              size: 50.0,
            ),
            const SizedBox(
              height: 32.0,
            ),
            const Text(
              "결제가 완료되었습니다.",
              textAlign: TextAlign.center,
            ),
            const SizedBox(
              height: 32.0,
            ),
            ElevatedButton(
              onPressed: () {
                context.replace(const HomeRoute().location);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: PRIMARY_COLOR,
                foregroundColor: Colors.white,
              ),
              child: const Text("홈으로"),
            )
          ],
        ),
      ),
    );
  }
}
