from pydantic import BaseModel

class FileEntry(BaseModel):
	name: str
	is_dir: bool
	size: int | None = None
