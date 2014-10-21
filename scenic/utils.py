
def store(name):
    """Memoizing decorator that caches the value on the ``state`` argument"""

    def decorator(func):
        def wrap(self, state, context):
            try:
                return getattr(state, name)
            except AttributeError:
                value = func(self, state, context)
                setattr(state, name, value)
                return value
        return wrap
    return decorator


