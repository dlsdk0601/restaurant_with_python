import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/ex/hook.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../api/schema.gen.dart';
import '../globals.dart';

part 'restaurant_screen.freezed.dart';
part 'restaurant_screen.g.dart';

class RestaurantScreen extends HookConsumerWidget {
  const RestaurantScreen({super.key});

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

      // add listener
      Future.microtask(() => pageController.addListener(controllerListener));
      // init
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
      padding: const EdgeInsets.symmetric(
        horizontal: 16.0,
      ),
      child: RefreshIndicator(
        onRefresh: () async {
          await ref.read(_modelStateProvider.notifier).initialize();
          await ref.read(_modelStateProvider.notifier).init();
        },
        child: ListView.separated(
          physics: const AlwaysScrollableScrollPhysics(),
          controller: pageController,
          itemCount: model.restaurantList.length,
          itemBuilder: (_, index) {
            return _RestaurantListItem.fromModel(
              model: model.restaurantList[index],
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

class _RestaurantListItem extends StatelessWidget {
  final Widget image;
  final String name;
  final List<String> tags;
  final int ratingsCount;
  final int deliveryTime;
  final int deliveryFee;
  final double ratings;

  final bool isDetail;
  final String? detail;

  final String? heroKey;

  const _RestaurantListItem({
    super.key,
    required this.image,
    required this.name,
    required this.tags,
    required this.ratingsCount,
    required this.deliveryTime,
    required this.deliveryFee,
    required this.ratings,
    this.isDetail = false,
    this.detail,
    this.heroKey,
  });

  factory _RestaurantListItem.fromModel({
    required RestaurantListResItem model,
  }) =>
      _RestaurantListItem(
        image: Image.network(
          'http://localhost:5001/api${model.bsset.url}',
          fit: BoxFit.cover,
        ),
        name: model.name,
        tags: model.tags,
        ratingsCount: model.ratingCount,
        deliveryTime: model.deliveryTime,
        deliveryFee: model.deliveryFee,
        ratings: model.rating,
      );

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        if (heroKey != null)
          Hero(
            tag: ObjectKey(heroKey),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(isDetail ? 0 : 12.0),
              child: image,
            ),
          ),
        if (heroKey == null)
          ClipRRect(
            borderRadius: BorderRadius.circular(isDetail ? 0 : 12.0),
            child: image,
          ),
        const SizedBox(
          height: 16.0,
        ),
        Padding(
          padding: EdgeInsets.symmetric(horizontal: isDetail ? 16.0 : 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                name,
                style: const TextStyle(
                  fontSize: 20.0,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(
                height: 8.0,
              ),
              Text(
                tags.join(' · '),
                style: const TextStyle(
                  color: BODY_TEXT_COLOR,
                  fontSize: 14.0,
                ),
              ),
              const SizedBox(
                height: 8.0,
              ),
              Row(
                children: [
                  _IconText(
                    icon: Icons.star,
                    label: ratings.toString(),
                  ),
                  renderDot(),
                  _IconText(
                    icon: Icons.receipt,
                    label: ratingsCount.toString(),
                  ),
                  renderDot(),
                  _IconText(
                    icon: Icons.timelapse_outlined,
                    label: "$deliveryTime 분",
                  ),
                  renderDot(),
                  _IconText(
                    icon: Icons.monetization_on,
                    label: deliveryFee == 0 ? "무료" : deliveryFee.toString(),
                  ),
                ],
              ),
              if (detail != null && isDetail)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  child: Text(detail!),
                )
            ],
          ),
        )
      ],
    );
  }

  Widget renderDot() {
    return const Padding(
      padding: EdgeInsets.symmetric(horizontal: 4.0),
      child: Text(
        " · ",
        style: TextStyle(
          fontSize: 12.00,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}

class _IconText extends StatelessWidget {
  final IconData icon;
  final String label;

  const _IconText({
    super.key,
    required this.icon,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          icon,
          color: PRIMARY_COLOR,
          size: 14.0,
        ),
        const SizedBox(
          width: 8.0,
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12.0,
            fontWeight: FontWeight.w500,
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
        restaurantList: [],
        page: 1,
        hasNext: true,
      );

  initialize() {
    state = state.copyWith(
      initialized: false,
      isFetching: false,
      restaurantList: [],
      page: 1,
      hasNext: true,
    );
  }

  @override
  Future<void> init() async {
    if (state.initialized) {
      return;
    }
    state = state.copyWith(
      restaurantList: [],
    );
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

    final res = await api.restaurantList(
      RestaurantListReq(page: page ?? 1),
    );

    if (res == null) {
      return;
    }

    final list = res.list.rows.map((e) => e.item);
    state = state.copyWith(
      initialized: true,
      isFetching: false,
      restaurantList: [...state.restaurantList, ...list],
      hasNext: res.list.hasNext,
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
    required List<RestaurantListResItem> restaurantList,
  }) = __Model;
}
