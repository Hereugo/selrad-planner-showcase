from drf_spectacular.utils import OpenApiResponse, extend_schema

DEFAULT_EXCEL_RESPONSE = {
    (
        200,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ): OpenApiResponse(
        description="Excel file response",
    )
}

DEFAULT_IMG_RESPONSE = {
    (200, "image/png"): OpenApiResponse(
        description="Image file response",
    )
}


def export_schema(
    methods=["get"],
    summary="",
    description="Export data to a file.",
    filters=True,
    parameters=None,
    responses=None,
):
    """
    Helper function to simplify extend_schema usage.
    """
    parameters = parameters or []
    responses = responses or {}

    return extend_schema(
        methods=methods,
        description=description,
        summary=summary,
        filters=filters,
        parameters=parameters,
        responses=responses,
    )
