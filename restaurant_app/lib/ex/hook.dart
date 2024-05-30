import 'package:flutter/cupertino.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

typedef InitModelNotifierBase<T extends InitModel> = Notifier<T>;

void useInitModel<T extends InitModel>(
    WidgetRef ref, Refreshable<T> refreshable) {
  useEffect(() {
    final model = ref.read(refreshable);
    Future(model.init);

    return () => Future(model.deInit);
  }, []);
}

mixin InitModel {
  Future<void> init();

  Future<void> deInit();
}

PageController useInitScrollController<T extends PageInitModel>(
  WidgetRef ref,
  Refreshable<T> refreshable,
) {
  final pageController = usePageController();

  useEffect(() {
    void controllerListener() async {
      if (pageController.offset >
          pageController.position.maxScrollExtent - 300) {
        await ref.read(refreshable).onNext();
      }
    }

    Future(() => pageController.addListener(controllerListener));

    return () {
      pageController.removeListener(controllerListener);
    };
  }, []);

  return pageController;
}

mixin PageInitModel {
  Future<void> init();

  Future<void> deInit();

  Future<void> onNext();
}
