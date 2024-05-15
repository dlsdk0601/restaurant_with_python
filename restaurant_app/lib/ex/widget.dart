import 'package:flutter/widgets.dart';

import 'collection.dart';

extension IterableWidgetExtension on Iterable<Widget> {
  List<Widget> joinWidget(Widget Function() joiner) {
    return join2(joiner).toList(growable: false);
  }

  List<Widget> verticalSpacing([double? spacing]) {
    return joinWidget(() => SizedBox(height: spacing ?? 8));
  }

  List<Widget> horizontalSpacing([double? spacing]) {
    return joinWidget(() => SizedBox(width: spacing ?? 8));
  }
}
