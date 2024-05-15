extension StringExtensio on String {
  String data(Map<String, dynamic> map) {
    final values = map.entries.map((e) => '${e.key}=${e.value}').join(', ');
    return '$this:$values';
  }
}
