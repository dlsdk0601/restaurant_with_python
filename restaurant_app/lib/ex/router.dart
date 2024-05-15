import 'package:flutter/widgets.dart';
import 'package:go_router/go_router.dart';

extension GoRouterExtension on GoRouter {
  BuildContext get _context {
    return configuration.navigatorKey.currentState!.context;
  }

  String get location {
    return GoRouterState.of(_context).uri.toString();
  }

  void apply(void Function(BuildContext context) go) {
    go(_context);
  }

  void popAll() {
    while (canPop()) {
      pop();
    }
  }

  void popTimes(int times) {
    while (canPop() && times > 0) {
      times--;
      pop();
    }
  }
}
