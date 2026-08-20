from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(
        self,
        data=None,
        message="",
        status_code=200,
        **kwargs,
    ):

        response_data = {
            "message": message,
            "success": True,
            "data": data,
            "status": status_code,
        }

        super().__init__(
            data=response_data,
            status=status_code,
            **kwargs,
        )
