from typing import TypeVar, Callable
from fastapi import FastAPI

DependencyT = TypeVar("DependencyT")
FactoryT = TypeVar("FactoryT", bound=Callable)
 

class DependencyCollector:
    def __init__(self) -> None:
        self.dependencies: dict[DependencyT, FactoryT] = {}
 
    def factory(self, dependency: DependencyT) -> Callable[[FactoryT], FactoryT]:
        def decorator(factory: FactoryT):
            self.add_factory(dependency, factory)
 
        return decorator
 
    def add_factory(self, dependency: DependencyT, factory: FactoryT) -> None:
        if dependency not in self.dependencies:
            self.dependencies[dependency] = factory
 
    def init_dependencies(self, app: FastAPI) -> None:
        for dependency, factory in self.dependencies.items():
            app.dependency_overrides[dependency] = factory
 
 
collector = DependencyCollector()