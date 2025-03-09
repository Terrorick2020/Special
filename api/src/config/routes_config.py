from app_types.routes_type import ApiRoutes


__api_routes_data = {
    "prefix": "/api",
    "hello": {
        "glob": "/hello",
        "inner": {
            "preview": "/",
        },
    },
    "parser": {
        "glob": "/parser",
        "inner": {
            "get_info": "/get-info",
            "parse_info": "/parse-info",
            "accamulation_info": "/accamulation-info",
        },
    },
}

api_routes = ApiRoutes( **__api_routes_data )
