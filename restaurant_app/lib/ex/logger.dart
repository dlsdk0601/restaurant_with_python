import 'dart:developer';

typedef FlutterLogger = void Function(
  String message, {
  Object? error,
  StackTrace? stackTrace,
});

FlutterLogger getLogger(String name) {
  return (String message, {Object? error, StackTrace? stackTrace}) {
    log(
      message,
      name: 'flutter:$name',
      error: error,
      stackTrace: stackTrace,
    );
  };
}
