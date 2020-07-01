import math
from typing import Union

from flask import request, url_for


def url_for_other_page(page: Union[int, str]) -> str:
    """Generate full url for other page of the same set of objects.

    :param page: page number
    :type page: Union[int, str]
    :return: url for page of the same object's set
    :rtype: str
    """
    args = request.view_args.copy()
    args['p'] = page
    return url_for(request.endpoint, **args)


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


def query_pagination(query, order, collection_name='posts'):
    page_size = 10
    page = get_page()
    obj_count = query.count()
    num_pages = math.ceil(obj_count / page_size)
    objects = query.order_by(order).paginate(page, page_size)
    return {
        'num_pages': num_pages,
        'page': page,
        collection_name: objects,
    }
