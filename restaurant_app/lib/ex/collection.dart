import 'package:collection/collection.dart';

extension IterableExtension<E> on Iterable<E> {
  Iterable<(bool, E)> withLast() {
    return mapIndexed((index, e) => (index + 1 == length, e));
  }

  Iterable<E> mapWhere(bool Function(E e) predicate, E Function(E e) mapper) {
    return map((e) => predicate(e) ? mapper(e) : e);
  }

  Iterable<E> join2(E Function() joiner) {
    return withLast().expand((e) {
      final (last, i) = e;
      return last ? [i] : [i, joiner()];
    });
  }
}

extension ListExtension<E> on List<E> {
  int get lastIndex {
    return length - 1;
  }

  E? getOrNull(int? index) {
    if (index == null || index >= length) {
      return null;
    }

    return this[index];
  }

  E? next(E? current) {
    if (current == null) {
      return null;
    }

    final index = indexOf(current);

    // 없다
    if (index < 0) {
      return null;
    }

    // overflow
    if (index + 1 >= length) {
      return null;
    }

    return this[index + 1];
  }

  E? nextWhere(bool Function(E element) test) {
    return next(firstWhereOrNull(test));
  }
}

extension MapExtension<K, V> on Map<K, V> {
  MapEntry<K, V>? getOrNull(K? key) {
    if (key == null) {
      return null;
    }

    final value = this[key];
    if (!containsKey(key) || value == null) {
      return null;
    }

    return MapEntry(key, value);
  }
}
