import 'package:flutter/material.dart';

import '../api/schema.gen.dart';
import '../color.dart';

class ProductListItemView extends StatelessWidget {
  final int pk;
  final Image image;
  final String name;
  final String detail;
  final int price;
  final int? count;

  final VoidCallback? onRemove;
  final VoidCallback? onAdd;

  const ProductListItemView({
    super.key,
    required this.pk,
    required this.image,
    required this.name,
    required this.detail,
    required this.price,
    this.count,
    this.onRemove,
    this.onAdd,
  });

  factory ProductListItemView.fromProductModel(
          {required ProductListResItem model}) =>
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
      );

  factory ProductListItemView.fromCartModel({
    required CartListResItem model,
    required VoidCallback onAdd,
    required VoidCallback onRemove,
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
        count: model.count,
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
        ),
        if (onRemove != null && onAdd != null && count != null)
          Padding(
            padding: const EdgeInsets.only(
              top: 8.0,
            ),
            child: _Footer(
              total: (count! * price).toString(),
              count: count!,
              onRemove: onRemove!,
              onAdd: onAdd!,
            ),
          )
      ],
    );
  }
}

class _Footer extends StatelessWidget {
  final String total;
  final int count;
  final VoidCallback onRemove;
  final VoidCallback onAdd;

  const _Footer({
    super.key,
    required this.total,
    required this.count,
    required this.onRemove,
    required this.onAdd,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Text(
            "총액 $total",
            style: const TextStyle(
              color: PRIMARY_COLOR,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        Row(
          children: [
            renderButton(icon: Icons.remove, onTap: onRemove),
            const SizedBox(
              width: 8.0,
            ),
            Text(
              count.toString(),
              style: const TextStyle(
                color: PRIMARY_COLOR,
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(
              width: 8.0,
            ),
            renderButton(icon: Icons.add, onTap: onAdd),
          ],
        )
      ],
    );
  }

  Widget renderButton({
    required IconData icon,
    required VoidCallback onTap,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8.0),
        border: Border.all(
          color: PRIMARY_COLOR,
          width: 1.0,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        child: Icon(
          icon,
          color: PRIMARY_COLOR,
        ),
      ),
    );
  }
}
