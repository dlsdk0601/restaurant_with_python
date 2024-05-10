open: setup
	nix-shell --run 'idea .'

setup:
	nix-shell --run 'flutter pub get'

watch: setup
	nix-shell --run 'dart run build_runner watch --delete-conflicting-outputs'

build-apk:
	nix-shell --run 'flutter clean && flutter pub get && dart run build_runner build --delete-conflicting-outputs'
	nix-shell --run 'flutter build apk --target lib/main_local.dart'
	rm -rf ./xsailr.apk
	cp build/app/outputs/flutter-apk/app-release.apk ./xsailr.apk

build-appbundle:
	flutter clean
	flutter pub get
	flutter pub run build_runner build --delete-conflicting-outputs
	flutter build apk
	flutter build appbundle
	open build/app/outputs/bundle/release


open-apk:
	open build/app/outputs/flutter-apk

open-appbundle:
	open build/app/outputs/bundle/release


adb-push-apk: build-apk
	adb push build/app/outputs/flutter-apk/app-release.apk sdcard/Download/XSAILR.apk
