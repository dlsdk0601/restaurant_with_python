import 'package:flutter/foundation.dart';
import 'package:logger/logger.dart';

final logger = Logger();

class Config {
  Config._();

  bool splashFadeIn = true;

  Level loggerLevel = kDebugMode ? Level.debug : Level.warning;

  late Uri apiServer = Uri.parse('http://localhost:5001/api');
}

final config = Config._();
