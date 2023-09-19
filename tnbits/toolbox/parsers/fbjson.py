# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    fbjson.py
#
try:
    import cjson
except Exception as e:
    print('`Warning: Could not load python-cjson. Using json instead.')
    # In case loading cjson failed, make one that uses json.
    class cjson:
        @classmethod
        def encode(cls, s):
            import json
            return json.dumps(s)
        @classmethod
        def decode(cls, s):
            import json
            return json.loads(s)
