from app.modules.module import Module
from app.modules.database import Database
from app.modules.memory import Memory

MODULES: dict[str, Module] = {"database": Database, "memory": Memory}
