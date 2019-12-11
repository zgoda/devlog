from typing import Union

from flask import request, url_for


def url_for_other_page(page: Union[int, str]) -> str:
    args = request.view_args.copy()
    args['p'] = page
    return url_for(request.endpoint, **args)


def get_page(arg_name: str = 'p') -> int:
    try:
        return int(request.args.get(arg_name, '1'))
    except ValueError:
        return 1
