from fastapi import FastAPI
from fastapi import HTTPException
from file_manager import FileManager, PathTraversalError


file_manager = FileManager()
app = FastAPI()

@app.get("/")
def root():
	return{"message": "NAS API is working"}

@app.get("/disk")
def disk():
	return file_manager.disk_usage()

@app.get("/files")
def files(path: str = "."):
	try:
		return file_manager.list_files(path)
	except PathTraversalError as e:
		raise HTTPException(
			status_code=403,
			detail = str(e)
		)
		
