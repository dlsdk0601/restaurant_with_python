import 'package:flutter/material.dart';

TextStyle textStyle({
  String? fontFamily,
  FontWeight? fontWeight,
  required double fontSize,
  double? letterSpacing,
  required double lineHeight,
  Color? color,
}) {
  return TextStyle(
    fontFamily: fontFamily,
    fontWeight: fontWeight,
    fontSize: fontSize,
    letterSpacing: letterSpacing,
    height: lineHeight / fontSize,
    color: color,
  );
}
