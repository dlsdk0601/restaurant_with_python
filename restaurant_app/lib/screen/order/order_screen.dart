import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/api/schema.gen.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/ex/dt.dart';
import 'package:restaurant_app/ex/hook.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../globals.dart';

part 'order_screen.freezed.dart';
part 'order_screen.g.dart';

class OrderScreen extends HookConsumerWidget {
  const OrderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final model = ref.watch(_modelStateProvider);
    final pageController = useInitScrollController<_ModelState>(
      ref,
      _modelStateProvider.notifier,
    );

    useEffect(() {
      // init
      Future.microtask(() => ref.read(_modelStateProvider.notifier).init());
      return null;
    }, []);

    if (!model.initialized) {
      return Container();
    }

    return Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: 16.0,
      ),
      child: RefreshIndicator(
        onRefresh: () async {
          await ref.read(_modelStateProvider.notifier).deInit();
          await ref.read(_modelStateProvider.notifier).init();
        },
        child: ListView.separated(
          physics: const AlwaysScrollableScrollPhysics(),
          controller: pageController,
          itemCount: model.orders.length,
          separatorBuilder: (_, index) {
            return const SizedBox(
              height: 16.0,
            );
          },
          itemBuilder: (_, index) {
            return OrderListItemView.fromModel(
              model: model.orders[index],
            );
          },
        ),
      ),
    );
  }
}

class OrderListItemView extends StatelessWidget {
  final DateTime orderDate;
  final Image image;
  final String name;
  final String productNames;
  final int price;

  const OrderListItemView({
    super.key,
    required this.orderDate,
    required this.image,
    required this.name,
    required this.productNames,
    required this.price,
  });

  factory OrderListItemView.fromModel({
    required OrderListResItem model,
  }) =>
      OrderListItemView(
        orderDate: model.orderDate,
        image: Image.network(
          'http://localhost:5001/api${model.image.url}',
          height: 50.0,
          width: 50.0,
          fit: BoxFit.cover,
        ),
        name: model.name,
        productNames: model.productNames.length < 2
            ? model.productNames.first
            : "${model.productNames.first} 외${model.productNames.length - 1}개",
        price: model.price,
      );

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text("${orderDate.d1} 주문 완료"),
        const SizedBox(
          height: 8.0,
        ),
        Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16.0),
              child: image,
            ),
            const SizedBox(
              width: 16.0,
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(fontSize: 14.0),
                ),
                Text(
                  "$productNames $price원",
                  style: const TextStyle(
                    color: BODY_TEXT_COLOR,
                    fontWeight: FontWeight.w300,
                  ),
                )
              ],
            )
          ],
        )
      ],
    );
  }
}

@riverpod
class _ModelState extends _$ModelState with PageInitModel {
  @override
  _Model build() => const _Model(
        initialized: false,
        isFetching: false,
        orders: [],
        page: 1,
        hasNext: true,
      );

  @override
  Future<void> init() async {
    if (state.initialized) {
      return;
    }

    state = state.copyWith(orders: []);

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

    final res = await api.orderList(OrderListReq(page: page ?? 1));

    if (res == null) {
      return;
    }

    final list = res.orders.rows.map((e) => e.item);
    state = state.copyWith(
      initialized: true,
      isFetching: false,
      orders: [...state.orders, ...list],
      hasNext: res.orders.hasNext,
      page: res.orders.page,
    );
  }

  @override
  Future<void> deInit() async {
    state = state.copyWith(
      initialized: false,
      isFetching: false,
      orders: [],
      page: 1,
      hasNext: true,
    );
  }
}

@freezed
class _Model with _$Model {
  const factory _Model({
    required bool initialized,
    required bool isFetching,
    required int page,
    required bool hasNext,
    required List<OrderListResItem> orders,
  }) = __Model;
}
