import uuid as py_uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ex.api import BaseModel
from was.model import Model


class Asset(Model):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='파일명')
    content_type: Mapped[str] = mapped_column(String(128), nullable=False, comment='미디어 종류 - ex) image/gif')
    uuid: 'Mapped[py_uuid.UUID]' = mapped_column(UUID(as_uuid=True), nullable=False, unique=True, comment='고유키')
    url: Mapped[str] = mapped_column(String(256), nullable=False, comment='웹 경로')
    download_url: Mapped[str] = mapped_column(String(256), nullable=False, comment='다운로드 경로')

    __table_args__ = ({'comment': '업로드 파일'},)

    @classmethod
    def new_(cls, name, content_type):
        asset_uuid = py_uuid.uuid4()

        object_name = str(asset_uuid) + '/' + name
        object_name = object_name.removeprefix('/')  # / 로 시작하면 안된다.

        asset = Asset()
        asset.name = name
        asset.content_type = content_type
        asset.uuid = asset_uuid
        asset.url = f'/{object_name}'
        asset.download_url = f'/{object_name}'

        return asset

    class Bsset(BaseModel):
        uuid: py_uuid.UUID
        name: str
        url: str
        download_url: str
        content_type: str

    def to_bsset(self) -> Bsset:
        return Asset.Bsset(
            uuid=self.uuid, name=self.name, url=self.url,
            download_url=self.download_url,
            content_type=self.content_type,
            size=self.size,
            duration=self.duration,
            thumbnail=self._create_thumbnail()
        )
