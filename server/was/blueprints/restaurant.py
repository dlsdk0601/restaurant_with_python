from ex.api import BaseModel, Res, ok, err
from ex.sqlalchemy_ex import Pagination, api_paginate
from was.blueprints import app, bg
from was.model import db
from was.model.asset import Asset
from was.model.product import Product
from was.model.restaurant import RestaurantPriceRange, Restaurant


class RestaurantListReq(BaseModel):
    page: int


class RestaurantListResItem(BaseModel):
    pk: int
    name: str
    bsset: Asset.Bsset
    price_range: RestaurantPriceRange
    rating: float
    rating_count: int
    delivery_time: int
    delivery_fee: int
    tags: list[str]

    @classmethod
    def from_model(cls, restaurant: Restaurant) -> 'RestaurantListResItem':
        return RestaurantListResItem(
            pk=restaurant.pk, name=restaurant.name, bsset=restaurant.main_image.to_bsset(),
            tags=restaurant.tag_list(), price_range=restaurant.price_range,
            rating=restaurant.rating, rating_count=restaurant.rating_count,
            delivery_time=restaurant.delivery_time, delivery_fee=restaurant.delivery_fee
        )


class RestaurantListRes(BaseModel):
    list: Pagination[RestaurantListResItem]


@app.api()
def restaurant_list(req: RestaurantListReq) -> Res[RestaurantListRes]:
    q = db.select(
        Restaurant
    ).order_by(Restaurant.pk)

    pagination = api_paginate(q, page=req.page, map_=RestaurantListResItem.from_model)

    return ok(RestaurantListRes(list=pagination))


class RestaurantShowReq(BaseModel):
    pk: int


class RestaurantShowProductListItem(BaseModel):
    pk: int
    name: str
    image: Asset.Bsset
    detail: str
    price: int

    @classmethod
    def from_model(cls, product: Product) -> 'RestaurantShowProductListItem':
        return RestaurantShowProductListItem(
            pk=product.pk, name=product.name, image=product.main_image.to_bsset(),
            detail=product.detail, price=product.price
        )


class RestaurantShowRes(BaseModel):
    pk: int
    name: str
    image: Asset.Bsset
    tags: list[str]
    price_range: RestaurantPriceRange
    ratings: float
    ratings_count: int
    delivery_time: int
    delivery_fee: int
    detail: str
    products: list[RestaurantShowProductListItem]
    cart_count: int


@app.api()
def restaurant_show(req: RestaurantShowReq) -> Res[RestaurantShowRes]:
    if bg.user is None:
        return err('로그인후 이용해주시기 바랍니다.')

    restaurant: Restaurant | None = db.session.execute(
        db.select(Restaurant).filter_by(pk=req.pk)
    ) \
        .scalar_one_or_none()

    if restaurant is None:
        return err('데이터가 조회되지 않습니다.')

    return ok(RestaurantShowRes(
        pk=restaurant.pk, name=restaurant.name, image=restaurant.main_image.to_bsset(),
        tags=restaurant.tag_list(), price_range=restaurant.price_range, ratings=restaurant.rating,
        ratings_count=restaurant.rating_count, delivery_time=restaurant.delivery_time,
        delivery_fee=restaurant.delivery_fee, detail=restaurant.detail,
        cart_count=bg.user.cart.total_count,
        products=list(map(lambda x: RestaurantShowProductListItem.from_model(x), restaurant.products))
    ))
