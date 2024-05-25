from ex.api import BaseModel, Res, ok, err
from ex.sqlalchemy_ex import Pagination, api_paginate
from was.blueprints import app
from was.model import db
from was.model.asset import Asset
from was.model.product import Product
from was.model.restaurant import RestaurantPriceRange


class ProductListReq(BaseModel):
    page: int


class ProductListResRestaurant(BaseModel):
    pk: int
    name: str
    image: Asset.Besst
    tags: list[str]
    price_range: RestaurantPriceRange
    ratings: float
    ratings_count: int
    delivery_time: int
    deliver_fee: int


class ProductListResItem(BaseModel):
    pk: int
    name: str
    image: Asset.Bsset
    price: int
    detail: str
    restaurant: ProductListResRestaurant

    @classmethod
    def from_model(cls, product: Product) -> 'ProductListResItem':
        return ProductListResItem(
            pk=product.pk, name=product.name, image=product.main_image.to_bsset(),
            price=product.price, detail=product.detail,
            restaurant=ProductListResRestaurant(
                pk=product.restaurant.pk, name=product.restaurant.name,
                image=product.restaurant.main_image.to_bsset(), tags=product.restaurant.tag_list(),
                price_range=product.restaurant.price_range,
                ratings=product.restaurant.rating, ratings_count=product.restaurant.rating_count,
                delivery_time=product.restaurant.delivery_time, deliver_fee=product.restaurant.deliver_fee,
            )
        )


class ProductListRes(BaseModel):
    products: Pagination[ProductListResItem]


@app.api()
def product_list(req: ProductListReq) -> Res[ProductListRes]:
    q = db.select(Product).order_by(Product.pk.desc())

    pagination = api_paginate(q, page=req.page, map_=ProductListResItem.from_model)

    return ok(ProductListRes(products=pagination))


class ProductShowReq(BaseModel):
    pk: int


class ProductShowRes(BaseModel):
    pk: int
    name: str
    image: Asset.Bsset
    price: int
    detail: str
    restaurant: ProductListResRestaurant

    @classmethod
    def from_model(cls, product: Product) -> 'ProductListResItem':
        return ProductListResItem(
            pk=product.pk, name=product.name, image=product.main_image.to_bsset(),
            price=product.price, detail=product.detail,
            restaurant=ProductListResRestaurant(
                pk=product.restaurant.pk, name=product.restaurant.name,
                image=product.restaurant.main_image.to_bsset(), tags=product.restaurant.tag_list(),
                price_range=product.restaurant.price_range,
                ratings=product.restaurant.rating, ratings_count=product.restaurant.rating_count,
                delivery_time=product.restaurant.delivery_time, deliver_fee=product.restaurant.deliver_fee,
            )
        )


@app.api()
def product_show(req: ProductShowReq) -> Res[ProductShowRes]:
    product: Product | None = db.session.execute(
        db.select(Product).where(Product.pk == req.pk)
    ) \
        .scalar_one_or_none()

    if product is None:
        return err('데이터가 조회되지 않습니다.')

    return ok(
        ProductShowRes(product=ProductShowRes.from_model(product))
    )
