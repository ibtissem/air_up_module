from odoo.http import Response
import json


class JSONResponse(Response):
    def __init__(self, *args, **kw):
        _data = kw.get('response') or {}
        _data = json.dumps(_data)
        super().__init__(*args, **kw)
        self.content_type = 'application/json'
        self.set_data(_data)

    def __str__(self):
        return self.get_data(as_text=True)
