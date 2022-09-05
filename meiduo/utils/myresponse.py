from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data=None, status=None, headers=None, exception=False, desc=None, code=2000, success=True,
                 **kwargs):

        dic = {'code': code, 'success': success, 'data': data}
        if desc is not None:
            dic['desc'] = desc
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers, exception=exception)
