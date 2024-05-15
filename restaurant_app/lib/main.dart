import 'package:flutter/material.dart';
import 'package:logger/logger.dart';

import 'application.dart';

void main() async {
  await runMain();
}

Future<void> runMain({
  String? initialLocation,
  Level logLevel = Level.warning,
  GlobalKey? providerScopeKey,
  GlobalKey? applicationKey,
}) async {
  Logger.level = logLevel;
  WidgetsFlutterBinding.ensureInitialized();

  runApplication(
    initialLocation: initialLocation,
    providerScopeKey: providerScopeKey,
    applicationKey: applicationKey,
  );
}

void restartApplication() {
  runApplication(
    providerScopeKey: GlobalKey(debugLabel: 'providerScope${DateTime.now()}'),
    applicationKey: GlobalKey(debugLabel: 'applicationScope${DateTime.now()}'),
  );
}
