import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/router.dart';
import 'package:restaurant_app/view/splash.dart';

class Application extends StatelessWidget {
  final GoRouter goRouter;

  const Application({super.key, required this.goRouter});

  @override
  Widget build(BuildContext context) {
    final darkThemeData = ThemeData(
      fontFamily: 'NotoSans',
    );
    final themeData = darkThemeData.copyWith();

    return MaterialApp.router(
      routerConfig: goRouter,
      themeMode: ThemeMode.dark,
      darkTheme: themeData,
      builder: transitionBuilderChain([
        SplashView.init(goRouter),
        EasyLoading.init(),
      ]),
    );
  }
}

void runApplication({
  String? initialLocation,
  GlobalKey? providerScopeKey,
  GlobalKey? applicationKey,
}) {
  runApp(
    ProviderScope(
      key: providerScopeKey,
      child: Application(
        key: applicationKey,
        goRouter: buildRouter(initialLocation: initialLocation),
      ),
    ),
  );
}

TransitionBuilder transitionBuilderChain(List<TransitionBuilder> builders) {
  return (context, child) {
    return builders.fold(child ?? Container(), (transitedChild, builder) {
      return builder(context, transitedChild);
    });
  };
}
