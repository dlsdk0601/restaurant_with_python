from ex.api import BaseModel, Res, ok
from ex.sqlalchemy_ex import Pagination, api_paginate
from was.blueprints import app
from was.model import db
from was.model.asset import Asset
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
    ).order_by(RestaurantListResItem.pk)

    pagination = api_paginate(q, page=req.page, map_=RestaurantListResItem.from_model)

    return ok(RestaurantListRes(list=pagination))
