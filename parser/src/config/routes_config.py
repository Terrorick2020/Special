from app_types.routes_type import ApiRoutes


__parser_routes_data = {
    "prefix": "/parser",
    "hello": {
        "glob": "/hello",
        "inner": {
            "preview": "/",
        },
    },
    "parse_info": {
        "glob": "/parse-info",
        "inner": {
            "preview": "/",
        },
    },
}

api_routes = ApiRoutes( **__parser_routes_data )