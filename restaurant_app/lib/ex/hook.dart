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
