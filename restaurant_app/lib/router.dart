import 'package:flutter/widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:restaurant_app/screen/home_screen.dart';
import 'package:restaurant_app/screen/intro.dart';
import 'package:restaurant_app/screen/sign_in_screen.dart';

part 'router.g.dart';

@TypedGoRoute<IntroRoute>(path: '/intro')
class IntroRoute extends GoRouteData {
  const IntroRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const IntroScreen();
  }
}

@TypedGoRoute<HomeRoute>(
  path: '/',
)
class HomeRoute extends GoRouteData {
  const HomeRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) => const HomeScreen();
}

@TypedGoRoute<SignInRoute>(
  path: '/sign-in',
)
class SignInRoute extends GoRouteData {
  const SignInRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) =>
      const SignInScreen();
}

const defaultLocation = '';

GoRouter buildRouter({String? initialLocation}) {
  return GoRouter(
    routes: $appRoutes,
    initialLocation:
        initialLocation == defaultLocation ? null : initialLocation,
  );
}
