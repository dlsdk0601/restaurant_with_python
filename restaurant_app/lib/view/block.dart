import 'package:flutter_easyloading/flutter_easyloading.dart';

int _counter = 0;

Future<T> block<T>(Future<T> Function() body) async {
  if (_counter++ == 0) {
    EasyLoading.show();
  }

  try {
    return await body();
  } finally {
    if (--_counter == 0) {
      EasyLoading.dismiss();
    }
  }
}
