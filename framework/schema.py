# framework/schema.py
#此文件定义了订单响应的 JSON Schema，用于验证 API 返回的数据结构是否符合预期
ORDER_SCHEMA = {
    "type": "object",
    "required": ["code", "msg", "data"],
    "properties": {
        "code": {"type": "integer"},
        "msg":  {"type": "string"},
        "data": {
            "type": "object",
            "required": ["order_id", "amount", "status"],
            "properties": {
                "order_id": {"type": "integer"},
                "amount":   {"type": "number"},
                "status":   {"type": "string", "enum": ["paid", "created"]},
            },
        },
    },
}