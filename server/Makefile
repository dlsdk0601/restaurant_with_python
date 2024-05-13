open: setup
	nix-shell --run 'pycharm .'

setup: venv
	venv/bin/pip install pip==23.2.1
	venv/bin/pip install -e .

venv:
	nix-shell --run 'python3.11 -m venv venv'

watch: setup
	venv/bin/dmypy restart
# watchmedo 는 최초 1회 실행이 없어서 그냥 먼저 실행한다.
# 실행 과정에서 오류가 발생해도 그냥 무시한다. 어차피 계속 실행되어야 한다.
	-$(MAKE) watch-run
	venv/bin/watchmedo shell-command --patterns="*.py;*.ini;*.tsx" --recursive --ignore-directories --drop --command='echo ""; make watch-run' .

# 파일 저장할 때마다 타입 체크
watch-run: code-gen mypy-check

# mypy 타입 체크
mypy-check:
# daemon mypy 로 webapp, ex 아래 소스들 체크
	venv/bin/dmypy run -- was ex bin

code-gen:
	#(source venv/bin/activate && $(MAKE) '_code-gen')

_code-gen:
	python bin/generate_api_ts_schema.py | python bin/tee.py ../tris-addee2-admin/src/api/schema.g.ts
	python bin/generate_api_ts.py | python bin/tee.py ../tris-addee2-admin/src/api/api.g.ts
	python bin/generate_api_dart_schema.py | (type dart > /dev/null && dart format || cat) | python bin/tee.py ../app/lib/api/schema.gen.dart
	python bin/generate_api_dart.py | (type dart > /dev/null && dart format || cat) | python bin/tee.py ../app/lib/api/api.gen.dart

# 개발용 테스트 데이터 DB 생성
faker-import:
	time venv/bin/python bin/faker_import.py

# 개발용 백그라운드 서비스 실행 (DB)
dev:
	docker compose up -d
	sleep 1

# 개발용 백그라운드 서비스 삭제 및 정리 (DB)
dev-clean:
	docker compose down -v --rmi local

# 개발용 백그라운드 서비스 초기화 및 샐행 (DB, alembic)
dev-reinitialize: dev-clean dev
	venv/bin/alembic upgrade head
	venv/bin/python bin/faker_import.py
