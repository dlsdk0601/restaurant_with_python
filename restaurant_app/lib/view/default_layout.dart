import 'package:flutter/material.dart';

class DefaultLayout extends StatelessWidget {
  final Color? backgroundColor;
  final Widget child;
  final String? title;
  final BottomNavigationBar? bottomNavigationBar;
  final Widget? floatingActionButton;

  const DefaultLayout({
    super.key,
    required this.child,
    this.backgroundColor,
    this.title,
    this.bottomNavigationBar,
    this.floatingActionButton,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: renderAppBar(),
      backgroundColor: backgroundColor ?? Colors.white,
      body: child,
      bottomNavigationBar: bottomNavigationBar,
      floatingActionButton: floatingActionButton,
    );
  }

  AppBar? renderAppBar() {
    if (title == null) {
      return null;
    }

    return AppBar(
      title: Text(
        title!,
        style: const TextStyle(
          fontSize: 16.0,
          fontWeight: FontWeight.w500,
        ),
      ),
      backgroundColor: Colors.white,
      elevation: 0, // 튀어 나온 느낌이 나오는 값
      foregroundColor: Colors.black,
    );
  }
}
