from fastapi import FastAPI, Form
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from file_manager import FileManager, PathTraversalError
from auth import(create_access_token, authenticate_user)
from schemas import FileEntry,  LoginRequest
from fastapi import Depends
from auth import get_current_user
from schemas import FileEntry
from monitor import ram_usage, cpu_usage, disk_usage, cpu_temp


file_manager = FileManager()
app = FastAPI()

app.mount(
	"/static",
	StaticFiles(directory = "static"),
	name = "static"
)

@app.get("/")
def root():
    return FileResponse("static/index.html")
    
@app.get("/disk")
def disk(user: str = Depends(get_current_user)):
	return file_manager.disk_usage()

@app.get("/files", response_model = list[FileEntry])
def files(path: str = ".", user: str = Depends(get_current_user)):
	try:
		return file_manager.list_files(path)
	except PathTraversalError as e:
		raise HTTPException(
			status_code=403,
			detail = str(e)
		)
		
@app.post("/mkdir")
def mkdir(path: str, user: str = Depends(get_current_user)):
	try:
		file_manager.create_dir(path)
		return {"message": "Directory Created"}
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)
		
@app.delete("/delete")
def delete(path: str, user: str = Depends(get_current_user)):
	try:
		file_manager.delete(path)
		return {"message": "Deleted"}
	except PathTraversalError as e:			
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)

@app.post("/rename")
def rename(old_path: str, new_path: str, user: str = Depends(get_current_user)):
	try:	
		file_manager.rename(old_path, new_path)
		return {"message": "Renamed"}
	except PathTraversalError as e:
		raise HTTPException(
			status_code = 403,
			detail = str(e)
		)

@app.get("/download")
def download(path: str, user: str = Depends(get_current_user)):
	
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
	destination: str = Form("."), 
	user: str = Depends(get_current_user)
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
		
@app.post("/auth/login")
def login(credentials: LoginRequest):

	user = authenticate_user(
		credentials.username,
		credentials.password
	)

	if not user:
		raise HTTPException(
			status_code=401,
			detail="Invalid credentials"
		)

	token = create_access_token(
		{"sub": user}
	)

	return {
		"access_token": token,
		"token_type": "bearer"
	}

@app.get("/monitor/ram")
def monitor_ram(
    user: str = Depends(get_current_user)
):
    return ram_usage()

@app.get("/monitor/cpu")
def monitor_cpu(
    user: str = Depends(get_current_user)
):
    return cpu_usage()

@app.get("/monitor/disk")
def monitor_disk(
    user: str = Depends(get_current_user)
):
    return disk_usage()

@app.get("/monitor/temp")
def monitor_temp(
    user: str = Depends(get_current_user)
):
    return cpu_temp()
    
@app.get("/login")
def login_page():
    return FileResponse(
        "static/login.html"
    )
