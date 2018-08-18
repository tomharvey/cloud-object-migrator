from contextlib import contextmanager
from types import ModuleType


class Config(ModuleType):
    """Set up the config object.

    When running a local command you should specify the path to a settings
    file which contains the values required of the local environment.
    """
    def update_from_file(self, filename):
        """Update the config Dict from a  file."""
        ns = {}
        with open(filename) as handle:
            code = compile(handle.read(), filename, 'exec')
            exec(code, ns)
        values = {
            key: value
            for key, value in ns.items()
            if not key.startswith('_')
        }
        self.__dict__.update(values)

    @contextmanager
    def override(self, **kwargs):
        original_values = {}
        missing = object()

        for key, value in kwargs.items():
            original_values[key] = getattr(self, key, missing)
            setattr(self, key, value)

        try:
            yield
        finally:
            for key, value in original_values.items():
                if value is missing:
                    delattr(self, key)
                else:
                    setattr(self, key, value)


config = Config('config')
