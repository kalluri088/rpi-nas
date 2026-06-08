let currentPath = ".";

function formatSize(bytes) {

    if (bytes < 1024)
        return `${bytes} B`;

    if (bytes < 1024 ** 2)
        return `${(bytes / 1024).toFixed(1)} KB`;

    if (bytes < 1024 ** 3)
        return `${(bytes / (1024 ** 2)).toFixed(1)} MB`;

    return `${(bytes / (1024 ** 3)).toFixed(1)} GB`;
}

async function loadFiles(path = ".") {

    currentPath = path;
	
	document.getElementById("currentPath").innerText = `Current Folder: ${path}`;
	
    const response =
        await fetch(`/files?path=${encodeURIComponent(path)}`);

    const files = await response.json();

    const table = document.getElementById("fileTable");

    table.innerHTML = "";

    files.forEach(file => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                ${
                    file.is_dir
                    ? `<a href="#" onclick="loadFiles('${currentPath}/${file.name}')">
                         📁 ${file.name}
                       </a>`
                    : file.name
                }
            </td>

            <td>${file.is_dir ? "-" : formatSize(file.size)}</td>

            <td>
                ${
                    file.is_dir
                    ? "Folder"
                    : `<a href="/download?path=${currentPath}/${file.name}">
                        Download
                       </a>

                       <button onclick="deleteFile('${currentPath}/${file.name}')">
                        Delete
                       </button>`
                }
            </td>
        `;

        table.appendChild(row);
    });
}

async function uploadFile() {

    console.log("1. Button clicked");

    const input = document.getElementById("fileInput");

    console.log("2. Input found:", input);

    if(input.files.length === 0){
        console.log("3. No file selected");
        return;
    }

    console.log("4. File selected:", input.files[0].name);

    const formData = new FormData();

    formData.append(
        "file",
        input.files[0]
    );

    console.log("5. Sending request");

    const response = await fetch(
        "/upload",
        {
            method: "POST",
            body: formData
        }
    );

    console.log("6. Response received:", response.status);

    if(response.ok){
        console.log("7. Upload successful");
        loadFiles();
    }
}

async function deleteFile(filename) {

    const response = await fetch(
        `/delete?path=${filename}`,
        {
            method: "DELETE"
        }
    );

    if(response.ok){
        loadFiles();
    }
}

async function loadDiskUsage() {

    const response = await fetch("/disk");

    const disk = await response.json();
    
    const totalGB = (disk.total / (1024**3)).toFixed(2);
    const usedGB = (disk.used / (1024**3)).toFixed(2);
    const free = (disk.free / (1024**3)).toFixed(2);
	
	const percentUsed = ((disk.used / disk.total) * 100).toFixed(2)
	document.getElementById("diskBar").value = percentUsed;
	
    document.getElementById("diskUsage").innerText =
        `Used: ${usedGB} GB <br>
         Total: ${totalGB} GB <br>`;
       
}

function goBack(){
		if(currentPath == "."){
			return;
		}
		
		const parts = currentPath.split("/");
		
		parts.pop();
		
		let parent;
		
		if(parts.length == 0){
				parent = ".";
		}
		else{
				parent = parts.join("/");
		}
		
		loadFiles(parent);
}

loadFiles();
loadDiskUsage();
