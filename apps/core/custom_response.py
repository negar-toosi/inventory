from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(
        self,
        data=None,
        message="",
        status_code=200,
        **kwargs,
    ):
        if status_code >= 400:
            response_data = {
                "data": data,
                "success": False,
                "message": message,
                "status": status_code,
            }
        response_data = {
            "data": data,
            "success": True,
            "message": message,
            "status": status_code,
        }

        super().__init__(
            data=response_data,
            status=status_code,
            **kwargs,
        )
