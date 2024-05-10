import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

extension AsyncSnapshotToValue<T> on AsyncSnapshot<T> {
  AsyncValue<T> get asyncValue {
    return switch (this) {
      AsyncSnapshot(connectionState: ConnectionState.waiting) =>
        const AsyncValue.loading(),
      AsyncSnapshot(hasData: true, data: final data) => data == null
          ? AsyncValue.error(
              StateError('hasData, but data is null'), StackTrace.current)
          : AsyncValue.data(data),
      //error
      AsyncSnapshot(
        hasError: true,
        error: final error,
        stackTrace: final stackTrace,
      ) =>
        (error == null)
            ? AsyncValue.error(StateError('hasError, but error is null'),
                stackTrace ?? StackTrace.current)
            : AsyncValue.error(error, stackTrace ?? StackTrace.current),
      AsyncSnapshot(connectionState: ConnectionState.none) =>
        throw StateError('cannot convert ConnectionState.none to AsyncValue'),
      _ => throw StateError('invalid state: $this'),
    };
  }
}
