import 'package:badges/badges.dart';
import 'package:flutter/material.dart' hide Badge;
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/api/schema.gen.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/router.dart';
import 'package:restaurant_app/screen/restaurant/restaurant_screen.dart';
import 'package:restaurant_app/view/default_layout.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../globals.dart';
import '../../view/product_card_view.dart';

part 'restaurant_show_screen.freezed.dart';
part 'restaurant_show_screen.g.dart';

typedef OnAddCart = Future<void> Function(int);

class RestaurantShowScreen extends HookConsumerWidget {
  const RestaurantShowScreen({super.key, required this.pk});

  final int pk;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pageController = usePageController();
    final model = ref.watch(_modelStateProvider);

    useEffect(() {
      Future.microtask(() => ref.read(_modelStateProvider.notifier).init(pk));

      return null;
    }, []);

    if (model.restaurant == null) {
      return Container();
    }

    return DefaultLayout(
      title: model.restaurant!.name,
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          if (context.mounted) {
            context.go(
              CartScreenRoute(model.restaurant!.pk).location,
            );
          }
        },
        backgroundColor: PRIMARY_COLOR,
        child: Badge(
          badgeContent: Text(
            model.cartCount.toString(),
            style: const TextStyle(
              color: PRIMARY_COLOR,
              fontSize: 10.0,
            ),
          ),
          badgeStyle: const BadgeStyle(
            badgeColor: Colors.white,
          ),
          child: const Icon(Icons.shopping_basket_outlined),
        ),
      ),
      child: CustomScrollView(
        controller: pageController,
        slivers: [
          renderTop(model: model.restaurant!),
          renderLabel(),
          renderProducts(
              products: model.restaurant!.products,
              restaurant: model.restaurant!,
              onAddCart: (int productPk) async {
                await ref
                    .read(_modelStateProvider.notifier)
                    .onAddCart(productPk);
              }),
        ],
      ),
    );
  }

  SliverToBoxAdapter renderTop({required RestaurantShowRes model}) {
    return SliverToBoxAdapter(
      child: RestaurantListItemView(
        image: Image.network(
          'http://localhost:5001/api${model.image.url}',
          fit: BoxFit.cover,
        ),
        name: model.name,
        tags: model.tags,
        ratingsCount: model.ratingsCount,
        deliveryTime: model.deliveryTime,
        deliveryFee: model.deliveryFee,
        ratings: model.ratings,
        isDetail: true,
      ),
    );
  }

  SliverPadding renderProducts({
    required List<RestaurantShowProductListItem> products,
    required RestaurantShowRes restaurant,
    required OnAddCart onAddCart,
  }) {
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) {
            final model = products[index];

            return InkWell(
              onTap: () async {
                await onAddCart(model.pk);
              },
              child: Padding(
                padding: const EdgeInsets.only(top: 8.0, bottom: 8.0),
                child:
                    ProductCardView.restaurantShowProductListItem(model: model),
              ),
            );
          },
          childCount: products.length,
        ),
      ),
    );
  }

  SliverPadding renderLabel() {
    return const SliverPadding(
      padding: EdgeInsets.symmetric(horizontal: 16.0),
      sliver: SliverToBoxAdapter(
        child: Text(
          "메뉴",
          style: TextStyle(fontSize: 18.0, fontWeight: FontWeight.w500),
        ),
      ),
    );
  }
}

@riverpod
class _ModelState extends _$ModelState {
  @override
  _Model build() => const _Model(
        initialized: false,
        pk: null,
        restaurant: null,
        cartCount: 0,
      );

  Future<void> init(int pk) async {
    final res = await api.restaurantShow(RestaurantShowReq(pk: pk));

    if (res == null) {
      return;
    }

    state = state.copyWith(
      initialized: true,
      restaurant: res,
      pk: res.pk,
      cartCount: res.cartCount,
    );
  }

  Future<void> onAddCart(int productPk) async {
    final res = await api.cartAdd(CartAddReq(productPk: productPk));

    if (res == null) {
      return;
    }

    state = state.copyWith(
      cartCount: res.totalCount,
    );
  }
}

@freezed
class _Model with _$Model {
  const factory _Model({
    required bool initialized,
    required int? pk,
    required RestaurantShowRes? restaurant,
    required int cartCount,
  }) = __Model;
}
