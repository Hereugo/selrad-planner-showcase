def http_methods_disable(*methods):
    def decorator(cls):
        cls.http_method_names = [
            method for method in cls.http_method_names if method not in methods
        ]
        return cls

    return decorator
