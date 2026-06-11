from pathlib import Path  #allows to handle file system paths using mordern, object oriented code instead of raw strings
import shutil #built in lib for high-level operations for copying, moving, renaming and removing files and directories
import os

from config import NAS_ROOT
from exceptions import PathTraversalError

class FileManager:
	
	base_path = Path(NAS_ROOT).resolve()
	
	def get_file_path(self, path: str):
		validated_path = self._validate_path(path)
		
		if not validated_path.is_file():
			raise FileNotFoundError()
			
		return validated_path
	
	def _validate_path(self, path:str) -> Path:
		requested_path = (self.base_path / path).resolve()
		
		if not requested_path.is_relative_to(self.base_path):
			raise PathTraversalError(
				f"Access outside NAS root: {path}"
			)
			
		return requested_path
		
	def list_files(self, path: str = "."):
		validated_path = self._validate_path(path)

		final_list_files_dir = []

		for i in validated_path.iterdir():

			if i.is_dir():
				dir_temp = {"name": i.name, "is_dir": True, "size": self.get_folder_size(i)}
				final_list_files_dir.append(dir_temp)
			else:
				file_temp = {"name": i.name, "is_dir": False, "size": i.stat().st_size}
				final_list_files_dir.append(file_temp)

		return final_list_files_dir
			
		
	def create_dir(self, path: str):
		validated_path = self._validate_path(path)
		validated_path.mkdir(
			parents = True,
			exist_ok = True
		)
		if(validated_path.exists()):
			return True
		else:
			return False
		
	def write_file(self, path: str, content_to_write: bytes):
		validated_path = self._validate_path(path)
		validated_parent_path = validated_path.parent
		validated_parent_path.mkdir(
			parents = True,
			exist_ok = True
		)
		with open(validated_path, "wb") as f:
			f.write(content_to_write)
		return True
		
	def read_file(self, path: str):
		validated_path = self._validate_path(path)
		if(validated_path.exists()):
			with open(validated_path, "rb") as f:
				return f.read()
				return
		else:
			raise FileNotFoundError(
				f"File Not Found: {path}"
			)
		
	def delete(self, path: str):
		validated_path = self._validate_path(path)
		if not validated_path.exists():
			raise FileNotFoundError(
				f"File Not Found: {path}"
			)
		if validated_path.is_dir():
			if not any(validated_path.iterdir()):
				validated_path.rmdir()
				return True
			else:
				raise OSError(
					"Directory is not empty"
				)
				return None
		else:
			validated_path.unlink()
			return True
		
	def rename(self, old_path: str, new_path: str):
		validated_source_path = self._validate_path(old_path)
		validated_dest_path = self._validate_path(new_path)
	
		if not validated_source_path.exists():
			raise FileNotFoundError(
					f"File Not Found: {old_path}"
			)
		validated_dest_path.parent.mkdir(
			parents = True,
			exist_ok = True
		)
		validated_source_path.rename(validated_dest_path)
		return True
		
	def save_upload(self, file, destination: str = "."):
		destination_path = self._validate_path(destination)
		
		if not destination_path.is_dir():
			raise NotADirectoryError(
				f"Not a Directory {destination}"
			)
			
		file_path = destination_path / file.filename
		
		with open(file_path, "wb") as buffer:
			shutil.copyfileobj(file.file,buffer)
			
		return {
				"filename": file.filename,
				"saved_to": str(file_path)
		}
		
	def get_folder_size(self, path):
		total_size = 0

		for root, dirs, files in os.walk(path):
			for file in files:
				file_path = Path(root) / file

				try:
					total_size += file_path.stat().st_size
				except OSError:
					pass

		return total_size
		
	def disk_usage(self):
		usage = shutil.disk_usage(NAS_ROOT)
		usage_directory = {"total":usage.total, "used":usage.used, "free":usage.free}
		return usage_directory
