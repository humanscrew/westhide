"""Simple helper to paginate query
"""
from flask import url_for, request

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def extract_pagination(query=None, page=None, per_page=None, **request_args):
    page = int(page) if page is not None else 1
    per_page = int(per_page) if per_page is not None else query.count()
    return page, per_page, request_args


def paginate(query, schema, link=None):
    page, per_page, other_request_args = extract_pagination(query, **request.args)
    page_obj = query.paginate(page=page, per_page=per_page)
    result = {
        "total": page_obj.total,
        "pages": page_obj.pages,
        "result": schema.dump(page_obj.items),
    }

    if link:
        next = url_for(
            request.endpoint,
            page=page_obj.next_num if page_obj.has_next else page_obj.page,
            per_page=per_page,
            **other_request_args,
            **request.view_args
        )
        prev = url_for(
            request.endpoint,
            page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
            per_page=per_page,
            **other_request_args,
            **request.view_args
        )
        result.update(next=next, prev=prev)

    return result
