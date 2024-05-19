import 'package:logger/logger.dart';
import 'package:restaurant_app/api/api.gen.dart';

import 'config.dart';

// 초기 실행 설정이 반영된 후 처리 되도록
// ignore: unnecessary_late
late final logger = Logger(level: config.loggerLevel, printer: PrettyPrinter());

// 초기 실행 설정이 반영된 후 처리 되도록
// ignore: unnecessary_late
late final api = Api(config.apiServer);
