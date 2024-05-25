from ex.api import BaseModel, Res, ok
from ex.sqlalchemy_ex import Pagination, api_paginate
from was.blueprints import app
from was.model import db
from was.model.asset import Asset
from was.model.product import Product


class ProductListReq(BaseModel):
    page: int


class ProductListResItem(BaseModel):
    pk: int
    name: str
    image: Asset.Bsset
    price: int
    detail: str
    restaurant_pk: int

    @classmethod
    def from_model(cls, product: Product) -> 'ProductListResItem':
        return ProductListResItem(
            pk=product.pk, name=product.name, image=product.main_image.to_bsset(),
            price=product.price, detail=product.detail, restaurant_pk=product.restaurant.pk
        )


class ProductListRes(BaseModel):
    products: Pagination[ProductListResItem]


@app.api()
def product_list(req: ProductListReq) -> Res[ProductListRes]:
    q = db.select(Product).order_by(Product.pk.desc())

    pagination = api_paginate(q, page=req.page, map_=ProductListResItem.from_model)

    return ok(ProductListRes(products=pagination))
