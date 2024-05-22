import 'package:flutter/material.dart';

import '../api/schema.gen.dart';
import '../color.dart';

class ProductCardView extends StatelessWidget {
  const ProductCardView({
    super.key,
    required this.pk,
    required this.image,
    required this.name,
    required this.detail,
    required this.price,
    this.onRemove,
    this.onAdd,
  });

  final int pk;
  final Image image;
  final String name;
  final String detail;
  final int price;

  final VoidCallback? onRemove;
  final VoidCallback? onAdd;

  factory ProductCardView.restaurantShowProductListItem({
    required RestaurantShowProductListItem model,
    VoidCallback? onRemove,
    VoidCallback? onAdd,
  }) =>
      ProductCardView(
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
                      // TextOverflow.ellipsis
                      // ... 처리
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
              )
            ],
          ),
        ),
      ],
    );
  }
}
