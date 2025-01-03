from functools import wraps

from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


def viewset_class(viewset_class: type[GenericViewSet]):
    """
    Decorator mainly for attaching function-based-views with class-based-view

    Access within kwargs, example:
    .. code-block:: python
    # Use the filterset_class decorator
    @api_view(['GET'])
    @viewset_class(PlanViewSet)
    def my_view(request, *args, **kwargs):
        # Access the filterset class from kwargs
        viewset_class = kwargs.get('viewset_class', None)
    """

    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            request: Request = args[0].request
            kwargs["viewset"] = viewset_class().as_view({"get": "list"})(request)
            return func(*args, **kwargs)

        return decorator

    return wrapper
