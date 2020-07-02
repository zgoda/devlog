import math
from typing import Union, Mapping

from flask import request, url_for
from peewee import Expression, ModelSelect


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


def query_pagination(
            query: ModelSelect, order: Expression, collection_name: str = 'posts'
        ) -> Mapping[str, Union[int, ModelSelect]]:
    """Paginate given query and return part of template context containing
    pagination result and some metadata like current page number and total
    number of pages.

    :param query: query object to be paginated
    :type query: ModelSelect
    :param order: result order expression
    :type order: Expression
    :param collection_name: key under which object collection will be
                            returned, defaults to 'posts'
    :type collection_name: str, optional
    :return: part of template context as dictionary, containing pagination
             result and some metadata
    :rtype: Mapping[str, Union[int, ModelSelect]]
    """
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
