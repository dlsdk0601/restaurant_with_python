import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/ex/hook.dart';
import 'package:restaurant_app/view/default_layout.dart';
import 'package:restaurant_app/view/product_list_item_view.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../api/schema.gen.dart';
import '../../globals.dart';

part 'cart_screen.freezed.dart';
part 'cart_screen.g.dart';

class CartScreen extends HookConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final model = ref.watch(_modelStateProvider);

    useEffect(() {
      Future.microtask(() => ref.read(_modelStateProvider.notifier).init());

      return null;
    }, []);

    if (!model.initialized) {
      return Container();
    }

    if (model.carts.isEmpty) {
      return const DefaultLayout(
        title: "장바구니",
        child: Center(
          child: Text("장바구니가 비었습니다."),
        ),
      );
    }

    return DefaultLayout(
        title: "장바구니",
        child: SafeArea(
          bottom: true,
          child: Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: 16.0,
            ),
            child: Column(
              children: [
                Expanded(
                  child: ListView.separated(
                    itemCount: model.carts.length,
                    separatorBuilder: (_, index) {
                      return const Divider(
                        height: 32.0,
                      );
                    },
                    itemBuilder: (_, index) {
                      final cart = model.carts[index];
                      return ProductListItemView.fromCartModel(
                        model: cart,
                        onAdd: () async {
                          await ref
                              .read(_modelStateProvider.notifier)
                              .onAdd(cart.productPk);
                        },
                        onRemove: () async {
                          await ref
                              .read(_modelStateProvider.notifier)
                              .onRemove(cart.productPk);
                        },
                      );
                    },
                  ),
                ),
                Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          "장바구니 금액",
                          style: TextStyle(
                            color: BODY_TEXT_COLOR,
                          ),
                        ),
                        Text("₩ ${model.totalPrice}")
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          "배달비",
                          style: TextStyle(
                            color: BODY_TEXT_COLOR,
                          ),
                        ),
                        if (model.carts.isNotEmpty)
                          Text("₩ ${(model.totalDeliveryFee).toString()}")
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          "총액",
                          style: TextStyle(
                            color: BODY_TEXT_COLOR,
                          ),
                        ),
                        Text(
                            "₩ ${(model.totalDeliveryFee + model.totalPrice).toString()}")
                      ],
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () async {
                          //   TODO :: order api
                          // 성공하면 orderDoneScreen 으로 실패하면 결제 실패 snackBar
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: PRIMARY_COLOR,
                        ),
                        child: const Text("결제 하기"),
                      ),
                    )
                  ],
                )
              ],
            ),
          ),
        ));
  }
}

@riverpod
class _ModelState extends _$ModelState with InitModel {
  @override
  _Model build() => const _Model(
        initialized: false,
        totalPrice: 0,
        totalDeliveryFee: 0,
        carts: [],
      );

  initialized() {
    deInit();
    init();
  }

  @override
  Future<void> init() async {
    if (state.initialized) {
      return;
    }

    final res = await api.cartList(const CartListReq());

    if (res == null) {
      return;
    }

    state = state.copyWith(
      initialized: true,
      totalDeliveryFee: res.totalDeliveryFee,
      totalPrice: res.totalPrice,
      carts: res.carts,
    );
  }

  @override
  Future<void> deInit() async {
    state = state.copyWith(
      initialized: false,
      carts: [],
      totalPrice: 0,
      totalDeliveryFee: 0,
    );
  }

  Future<void> onAdd(int productPk) async {
    final res = await api.cartAdd(CartAddReq(productPk: productPk));

    if (res == null) {
      return;
    }

    initialized();
  }

  Future<void> onRemove(int productPk) async {
    final res = await api.cartRemove(CartRemoveReq(productPk: productPk));

    if (res == null) {
      return;
    }

    initialized();
  }

  // TODO :: order API 추가
}

@freezed
class _Model with _$Model {
  const factory _Model({
    required bool initialized,
    required int totalPrice,
    required int totalDeliveryFee,
    required List<CartListResItem> carts,
  }) = __Model;
}
