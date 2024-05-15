import 'dart:math';

extension RageInt on Random {
  int rageInt({
    required int min,
    required int max,
  }) {
    return min + Random().nextInt(max - min + 1);
  }
}

extension RangeDouble on Random {
  double rangeDouble({
    required double min,
    required double max,
  }) {
    return Random().nextDouble() * (max - min + 1) + min;
  }
}
