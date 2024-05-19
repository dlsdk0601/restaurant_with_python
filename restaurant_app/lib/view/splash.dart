import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/view/default_layout.dart';
import 'package:restaurant_app/view/intro.dart';

import '../config.dart';
import '../model/user.dart';
import '../router.dart';

class SplashView extends HookConsumerWidget {
  const SplashView({
    super.key,
    required this.goRouter,
    required this.child,
  });

  final GoRouter goRouter;
  final Widget child;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final initialized = useState(false);
    useState(false);

    useEffect(() {
      var disposed = false;
      final startAt = DateTime.now();

      Future(() async {
        await userModel.init();

        if (disposed) return;

        if (userModel.userInfo == null) {
          if (context.mounted) {
            goRouter.go(const SignInRoute().location);
          } else {
            logger.w('cannot move to intro screen. context is not mounted.');
          }
        }

        if (config.splashFadeIn) {
          final endAt = DateTime.now();
          final wait = const Duration(seconds: 1) - endAt.difference(startAt);
          if (wait > Duration.zero) {
            await Future.delayed(wait);
          }
        }

        if (disposed) return;
        initialized.value = true;
      });

      return () {
        disposed = true;
      };
    }, []);

    return IntroSwitchView(
      child: !initialized.value
          ? _SplashImageView()
          : Container(
              key: _contentViewKey,
              child: child,
            ),
    );
  }

  static TransitionBuilder init(GoRouter goRouter) {
    return (context, child) {
      return SplashView(
        goRouter: goRouter,
        child: child ?? const SizedBox(),
      );
    };
  }
}

final _splashImageViewKey = GlobalKey(debugLabel: 'SplashImageViewKey');
final _contentViewKey = GlobalKey(debugLabel: 'ContentViewKey');

class _SplashImageView extends StatelessWidget {
  _SplashImageView() : super(key: _splashImageViewKey);

  @override
  Widget build(BuildContext context) {
    return DefaultLayout(
      backgroundColor: PRIMARY_COLOR,
      child: SizedBox(
        width: MediaQuery.of(context).size.width,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'asset/img/logo/logo.png',
              width: MediaQuery.of(context).size.width / 2,
            ),
            const SizedBox(
              height: 16.0,
            ),
            const CircularProgressIndicator(
              color: Colors.white,
            )
          ],
        ),
      ),
    );
  }
}
