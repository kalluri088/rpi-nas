from fastapi import FastAPI
from fastapi import HTTPException, UploadFile, File
from file_manager import FileManager, PathTraversalError
from schemas import FileEntry
from fastapi.responses import FileResponse

file_manager = FileManager()
app = FastAPI()

@app.get("/")
def root():
	return{"message": "NAS API is working"}

@app.get("/disk")
def disk():
	return file_manager.disk_usage()

@app.get("/files", response_model = list[FileEntry])
def files(path: str = "."):
	try:
		return file_manager.list_files(path)
	except PathTraversalError as e:
		raise HTTPException(
			status_code=403,
			detail = str(e)
		)
		
@app.post("/mkdir")
def mkdir(path: str):
	try:
		file_manager.create_dir(path)
		return {"message": "Directory Created"}
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)
		
@app.delete("/delete")
def delete(path: str):
	try:
		file_manager.delete(path)
		return {"message": "Deleted"}
	except PathTraversalError as e:			
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)

@app.post("/rename")
def rename(old_path: str, new_path: str):
	try:	
		file_manager.rename(old_path, new_path)
		return {"message": "Renamed"}
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)

@app.get("/download")
def download(path: str):
	
	try:
		file_path = file_manager.get_file_path(path)
		return FileResponse(
			path = file_path,
			filename = file_path.name
		)
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)
		
	except FileNotFoundError as e:
		raise HTTPException(
			status_code = 404,
			detail = str(e)
		)

@app.post("/upload")
def upload(
	file: UploadFile = File(...),
	destination: str = '.'
):
	try:
		return file_manager.save_upload(
			file,
			destination
		)
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)
		
	except FileNotFoundError as e:
		raise HTTPException(
			status_code = 404,
			detail = str(e)
		) 
		 
	




		
