import 'package:flutter/material.dart';
import 'package:restaurant_app/color.dart';

class CustomTextFormField extends StatelessWidget {
  final String? hintText;
  final String? errorText;
  final bool obscureText;
  final bool autoFocus;
  final ValueChanged<String> onChanged;

  const CustomTextFormField({
    super.key,
    required this.onChanged,
    this.hintText,
    this.errorText,
    this.obscureText = false,
    this.autoFocus = false,
  });

  @override
  Widget build(BuildContext context) {
    const baseBorder = OutlineInputBorder(
      borderSide: BorderSide(
        color: INPUT_BORDER_COLOR,
        width: 1.0,
      ),
    );

    return TextFormField(
      cursorColor: PRIMARY_COLOR,
      obscureText: obscureText,
      autofocus: autoFocus,
      onChanged: onChanged,
      decoration: InputDecoration(
        contentPadding: const EdgeInsets.all(20),
        hintText: hintText,
        hintStyle: const TextStyle(color: BODY_TEXT_COLOR, fontSize: 14.0),
        errorText: errorText,
        fillColor: INPUT_BG_COLOR,
        filled: true,
        border: baseBorder,
        focusedBorder: baseBorder.copyWith(
            borderSide: baseBorder.borderSide.copyWith(
          color: PRIMARY_COLOR,
        )),
        enabledBorder: baseBorder,
      ),
    );
  }
}
