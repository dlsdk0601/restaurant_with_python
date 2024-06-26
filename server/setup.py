from setuptools import setup, find_packages

setup(
    name="restaurant_was",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # was
        'Flask==3.0.3',
        'werkzeug==3.0.3',
        'sconfig==0.0.3',
        'pydantic==1.10.14',
        'stringcase==1.2.0',
        'Flask-Cors==4.0.1',
        # 데이터베이스
        'SQLAlchemy==2.0.30',
        'Flask-SQLAlchemy==3.1.1',
        'alembic==1.13.1',
        'psycopg2-binary==2.9.9',
        'coint-paginatify-sqlalchemy==0.0.4',
        'Faker==17.0.0',
        # ex
        'pytz==2024.1',
        'types-pytz==2024.1.0.20240417',
        'more-itertools==10.2.0',
        # 정적 타입 분석
        'mypy==1.10.0',
        'watchdog==4.0.0',
        'boto3==1.34.102',
        'requests==2.31.0',
        'types-requests==2.31.0.20240406',
        # 썸네일
        'Pillow==10.3.0',
    ],
)
