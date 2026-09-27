# generated — auto-loads every *_tool.py so agents can
# self.tools.call() them without explicit imports
import importlib
import pkgutil

for _module in pkgutil.iter_modules(__path__):
    if _module.name.endswith("_tool"):
        importlib.import_module(f".{_module.name}", package=__name__)
