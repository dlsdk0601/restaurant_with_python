import 'package:flutter/material.dart';
import 'package:restaurant_app/color.dart';
import 'package:restaurant_app/screen/product/product_list_screen.dart';
import 'package:restaurant_app/screen/restaurant/restaurant_screen.dart';
import 'package:restaurant_app/view/default_layout.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen>
    with SingleTickerProviderStateMixin {
  int index = 0;

  late TabController tabController;
  final List<_NavigationMenu> menus = const [
    _NavigationMenu(
      icon: Icons.home_outlined,
      name: '홈',
    ),
    _NavigationMenu(
      icon: Icons.fastfood_outlined,
      name: '음식',
    ),
    _NavigationMenu(
      icon: Icons.receipt_long_outlined,
      name: '주문',
    ),
    _NavigationMenu(
      icon: Icons.person_outline,
      name: '프로필',
    ),
  ];

  @override
  void initState() {
    super.initState();
    tabController = TabController(length: 4, vsync: this);

    tabController.addListener(tabListener);
  }

  @override
  void dispose() {
    tabController.dispose();
    super.dispose();
  }

  void tabListener() {
    setState(() {
      index = tabController.index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultLayout(
      title: menus[index].name,
      bottomNavigationBar: BottomNavigationBar(
        selectedItemColor: PRIMARY_COLOR,
        unselectedItemColor: BODY_TEXT_COLOR,
        selectedFontSize: 10,
        unselectedFontSize: 10,
        type: BottomNavigationBarType.shifting,
        onTap: (int index) {
          tabController.animateTo(index);
        },
        currentIndex: index,
        items: menus
            .map(
              (e) => BottomNavigationBarItem(
                icon: Icon(e.icon),
                label: e.name,
              ),
            )
            .toList(),
      ),
      child: TabBarView(
        physics: const NeverScrollableScrollPhysics(),
        controller: tabController,
        children: const [
          RestaurantScreen(),
          ProductListScreen(),
          Center(
            child: Text("주문"),
          ),
          Center(
            child: Text("프로필"),
          ),
        ],
      ),
    );
  }
}

class _NavigationMenu {
  final String name;
  final IconData icon;

  const _NavigationMenu({
    required this.name,
    required this.icon,
  });
}
