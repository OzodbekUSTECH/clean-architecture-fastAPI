from typing import Protocol

class IBlogsRepository(Protocol):
    async def save_blog(self, data: dict) -> None: ...
 
    async def get_blog(self, id: int) ->  None: ...
