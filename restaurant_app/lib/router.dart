import 'package:flutter/widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:restaurant_app/screen/intro.dart';

part 'router.g.dart';

@TypedGoRoute<IntroRoute>(path: '/intro')
class IntroRoute extends GoRouteData {
  const IntroRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const IntroScreen();
  }
}

const defaultLocation = '';

GoRouter buildRouter({String? initialLocation}) {
  return GoRouter(
    routes: $appRoutes,
    initialLocation:
        initialLocation == defaultLocation ? null : initialLocation,
  );
}
