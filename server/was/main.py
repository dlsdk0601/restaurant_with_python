from was import config
from was.application import app

# 운영 환경 중에서도 실제 실행시에만 초기화 한다.
# docker image 빌드시에 초기화를 시도하면 환경 변수가 없어서 에러가 발생한다.

if __name__ == '__main__':
    app.run(port=config.PORT, host='0.0.0.0', debug=config.DEBUG)
