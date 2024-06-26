from uuid import UUID

from flask import abort, send_file

from was.blueprints import app
from was.model import db
from was.model.asset import Asset


@app.route('/asset/<uuid:uuid>/<filename>')
def asset_show(uuid: UUID, filename: str):
    asset: Asset | None = db.session.execute(
        db.select(Asset).filter_by(uuid=uuid, name=filename)
    ) \
        .scalar_one_or_none()

    if asset is None:
        return abort(404)

    file_path = Asset.get_file_path(filename=asset.name)
    return send_file(file_path, mimetype=asset.content_type)
