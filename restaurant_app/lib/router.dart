import 'package:flutter/widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:restaurant_app/screen/home_screen.dart';
import 'package:restaurant_app/screen/product/product_list_screen.dart';
import 'package:restaurant_app/screen/restaurant/restaurant_show_screen.dart';
import 'package:restaurant_app/screen/sign_in_screen.dart';

part 'router.g.dart';

@TypedGoRoute<HomeRoute>(
  path: '/',
  routes: [
    TypedGoRoute<RestaurantShowRoute>(path: 'restaurant-show/:pk'),
    TypedGoRoute<ProductListRoute>(path: "product-list"),
  ],
)
class HomeRoute extends GoRouteData {
  const HomeRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) => const HomeScreen();
}

class RestaurantShowRoute extends GoRouteData {
  const RestaurantShowRoute(this.pk);

  final int pk;

  @override
  Widget build(BuildContext context, GoRouterState state) =>
      RestaurantShowScreen(pk: pk);
}

class ProductListRoute extends GoRouteData {
  const ProductListRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) =>
      const ProductListScreen();
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
