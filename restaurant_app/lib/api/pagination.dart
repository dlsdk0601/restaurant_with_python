// ignore_for_file: override_on_non_overriding_member

import 'package:freezed_annotation/freezed_annotation.dart';

part 'pagination.freezed.dart';
part 'pagination.g.dart';

@Freezed(genericArgumentFactories: true)
class PageRow<T> with _$PageRow<T> {
  const factory PageRow({required int no, required T item}) = _PageRow;

  factory PageRow.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) =>
      _$PageRowFromJson(json, fromJsonT);
}

@Freezed(genericArgumentFactories: true)
class Pagination<T> with _$Pagination<T> {
  const factory Pagination({
    required int page,
    required List<int> pages,
    required int prevPage,
    required int nextPage,
    required bool hasPrev,
    required bool hasNext,
    required int total,
    required T rows,
  }) = _Pagination;

  factory Pagination.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) =>
      _$PaginationFromJson(json, fromJsonT);
}

Pagination<List<PageRow<T>>> paginationFromJson<T>(
  Map<String, Object?> json,
  T Function(Map<String, Object?> map) itemFromJson,
) {
  return Pagination.fromJson(json, (rawRows) {
    return (rawRows as List<dynamic>).map((e) {
      return PageRow<T>.fromJson(
        e,
        (item) => itemFromJson(item as Map<String, Object?>),
      );
    }).toList();
  });
}

mixin ToJson {
  Map<String, dynamic> toJson();
}

mixin PaginationConverter<T extends ToJson> {
  T Function(Map<String, Object?> json) getFromJson();

  @override
  Pagination<List<PageRow<T>>> fromJson(Map<String, Object?> json) {
    return paginationFromJson(json, getFromJson());
  }

  @override
  Map<String, Object?> toJson(Pagination<List<PageRow<T>>> object) {
    return object.toJson(
      (rows) => rows.map(
        (pageRow) => pageRow.toJson(
          (p0) => p0.toJson(),
        ),
      ),
    );
  }
}
