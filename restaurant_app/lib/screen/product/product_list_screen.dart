import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/ex/hook.dart';
import 'package:restaurant_app/router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../api/schema.gen.dart';
import '../../globals.dart';

part 'product_list_screen.freezed.dart';
part 'product_list_screen.g.dart';

class ProductListScreen extends HookConsumerWidget {
  const ProductListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pageController = usePageController();
    final model = ref.watch(_modelStateProvider);

    useEffect(() {
      bool isFetching = false;

      void controllerListener() async {
        if (pageController.offset >
            pageController.position.maxScrollExtent - 300) {
          if (!isFetching) {
            isFetching = true;
            await ref.read(_modelStateProvider.notifier).onNext();
            isFetching = false;
          }
        }
      }

      Future.microtask(() => pageController.addListener(controllerListener));
      Future.microtask(() => ref.read(_modelStateProvider.notifier).init());

      return () {
        pageController.removeListener(controllerListener);
        pageController.dispose();
      };
    }, []);

    if (!model.initialized) {
      return Container();
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: RefreshIndicator(
        onRefresh: () async {
          await ref.read(_modelStateProvider.notifier).initialize();
          await ref.read(_modelStateProvider.notifier).init();
        },
        child: ListView.separated(
          physics: const AlwaysScrollableScrollPhysics(),
          controller: pageController,
          itemCount: model.products.length,
          itemBuilder: (_, index) {
            return GestureDetector(
              onTap: () {
                final pk = model.products[index].restaurantPk;
                // 상품 클릭하면 결국엔 레스토랑 상세 페이지로
                context.go(RestaurantShowRoute(pk).location);
              },
              child: ProductListItemView.fromProductModel(
                model: model.products[index],
              ),
            );
          },
          separatorBuilder: (_, index) {
            return const SizedBox(
              height: 16.0,
            );
          },
        ),
      ),
    );
  }
}

class ProductListItemView extends StatelessWidget {
  final int pk;
  final Image image;
  final String name;
  final String detail;
  final int price;

  final VoidCallback? onRemove;
  final VoidCallback? onAdd;

  const ProductListItemView({
    super.key,
    required this.pk,
    required this.image,
    required this.name,
    required this.detail,
    required this.price,
    this.onRemove,
    this.onAdd,
  });

  factory ProductListItemView.fromProductModel({
    required ProductListResItem model,
    VoidCallback? onRemove,
    VoidCallback? onAdd,
  }) =>
      ProductListItemView(
        pk: model.pk,
        image: Image.network(
          'http://localhost:5001/api${model.image.url}',
          width: 110,
          height: 110,
          fit: BoxFit.cover,
        ),
        name: model.name,
        detail: model.detail,
        price: model.price,
        onAdd: onAdd,
        onRemove: onRemove,
      );

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        IntrinsicHeight(
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(8.0),
                child: image,
              ),
              const SizedBox(
                width: 16.0,
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      name,
                      style: const TextStyle(
                        fontSize: 18.0,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Text(
                      detail,
                      overflow: TextOverflow.ellipsis,
                      maxLines: 2,
                      style: const TextStyle(
                        color: BODY_TEXT_COLOR,
                        fontSize: 14.0,
                      ),
                    ),
                    Text(
                      "₩$price",
                      textAlign: TextAlign.right,
                      style: const TextStyle(
                        color: PRIMARY_COLOR,
                        fontSize: 12.0,
                        fontWeight: FontWeight.w500,
                      ),
                    )
                  ],
                ),
              ),
            ],
          ),
        )
      ],
    );
  }
}

@riverpod
class _ModelState extends _$ModelState with InitModel {
  @override
  _Model build() => const _Model(
        initialized: false,
        isFetching: false,
        page: 1,
        hasNext: true,
        products: [],
      );

  initialize() {
    state = state.copyWith(
      initialized: false,
      isFetching: false,
      page: 1,
      hasNext: true,
      products: [],
    );
  }

  @override
  Future<void> init() async {
    if (state.initialized) {
      return;
    }
    state = state.copyWith(products: []);

    await onFetch(null);
  }

  Future<void> onNext() async {
    if (state.isFetching) {
      return;
    }

    await onFetch(state.page + 1);
  }

  Future<void> onFetch(int? page) async {
    state = state.copyWith(
      isFetching: true,
    );

    if (!state.hasNext) {
      return;
    }

    final res = await api.productList(ProductListReq(page: page ?? 1));

    if (res == null) {
      return;
    }

    final list = res.products.rows.map((e) => e.item);
    state = state.copyWith(
      initialized: true,
      isFetching: false,
      hasNext: res.products.hasNext,
      page: res.products.page,
      products: [...state.products, ...list],
    );
  }

  @override
  Future<void> deInit() async {}
}

@freezed
class _Model with _$Model {
  const factory _Model({
    required bool initialized,
    required bool isFetching,
    required int page,
    required bool hasNext,
    required List<ProductListResItem> products,
  }) = __Model;
}
