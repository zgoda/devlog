import math
from typing import Optional, Union

from flask import request, url_for
from peewee import ModelSelect


def url_for_other_page(page: Union[int, str]) -> str:
    """Generate full url for other page of the same set of objects.

    :param page: page number
    :type page: Union[int, str]
    :return: url for page of the same object's set
    :rtype: str
    """
    args = request.view_args.copy()  # type: ignore
    args['p'] = page
    return url_for(request.endpoint, **args)  # type: ignore


def get_page(arg_name: str = 'p') -> int:
    """Get page number from request params or return default which is 1.

    :param arg_name: URL param name, defaults to 'p'
    :type arg_name: str, optional
    :return: page number
    :rtype: int
    """
    try:
        return int(request.args.get(arg_name, '1'))
    except ValueError:
        return 1


class Pagination:

    def __init__(
                self, query: ModelSelect, count: Optional[int] = None,
                page: Optional[int] = None, page_size: Optional[int] = None,
            ):
        self.query = query
        self.page = page or get_page()
        self.page_size = page_size or 10
        obj_count = count or query.count()  # type: ignore
        self.pages = math.ceil(obj_count / self.page_size)
        self.has_next = self.pages > self.page
        self.has_prev = self.page > 1
        self.next_page = self.page + 1
        self.prev_page = self.page - 1

    @property
    def items(self):
        return self.query.paginate(self.page, self.page_size)
