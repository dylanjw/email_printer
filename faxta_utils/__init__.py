import functools


def apply_to_return_value(callback):
    def outer(fn):
        # We would need to type annotate *args and **kwargs but doing so segfaults
        # the PyPy builds. We ignore instead.
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return callback(fn(*args, **kwargs))

        return inner

    return outer

to_tuple = apply_to_return_value(
    tuple
)
