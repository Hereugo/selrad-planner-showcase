from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema

DEFAULT_FILE_RESPONSE = {
    200: OpenApiResponse(
        description="Download file response", response=OpenApiTypes.BINARY
    )
}
