let currentPath = ".";

if (!localStorage.getItem("token")) {
    window.location.href = "/login";
}

function authHeaders() {

    const token = localStorage.getItem("token");

    console.log("TOKEN:", token);

    return {
        Authorization: `Bearer ${token}`
    };
}

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

    document.getElementById("currentPath").innerText =
        `Current Folder: ${path}`;

    const response = await fetch(
        `/files?path=${encodeURIComponent(path)}`,
        { headers: authHeaders() }
    );

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

            <td>${formatSize(file.size)}</td>

            <td>
                ${
                    file.is_dir
                    ? "Folder"
                    :  `<button onclick="downloadFile('${currentPath}/${file.name}')">
							Download
						 </button>

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
    
    formData.append(
		"destination",
		currentPath
	);

	for (const pair of formData.entries()) {
		console.log(pair[0], pair[1]);
	}
	
    console.log("5. Sending request");

    const response = await fetch("/upload", {method: "POST", headers: authHeaders(), body: formData});

    console.log("6. Response received:", response.status);

    if(response.ok){
        console.log("7. Upload successful");
        loadFiles();
    }
}

async function deleteFile(filename) {

    const response = await fetch(`/delete?path=${filename}`, {method: "DELETE", headers: authHeaders()});

    if(response.ok){
        loadFiles();
    }
}

async function loadDiskUsage() {

    const response = await fetch("/disk", {headers: authHeaders()});

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

async function loadMonitoring() {

    const headers = authHeaders();

    const cpu =
        await fetch(
            "/monitor/cpu",
            { headers }
        );

    const ram =
        await fetch(
            "/monitor/ram",
            { headers }
        );

    const temp =
        await fetch(
            "/monitor/temp",
            { headers }
        );

    const disk =
        await fetch(
            "/monitor/disk",
            { headers }
        );

    const cpuData = await cpu.json();
    const ramData = await ram.json();
    const tempData = await temp.json();
    const diskData = await disk.json();

    document.getElementById("cpu").textContent =
        `${cpuData.cpu_percent}%`;

    document.getElementById("ram").textContent =
        `${ramData.percent}%`;

    document.getElementById("temp").textContent =
        `${tempData.temperature_c}°C`;

    const usedGB =
        (diskData.used / 1024**3).toFixed(1);

    const totalGB =
        (diskData.total / 1024**3).toFixed(1);

    document.getElementById("disk").textContent =
        `${usedGB} / ${totalGB} GB`;
}

async function downloadFile(path) {

    const response = await fetch(
        `/download?path=${encodeURIComponent(path)}`,
        {
            headers: authHeaders()
        }
    );

    if (!response.ok) {
        alert("Download failed");
        return;
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = path.split("/").pop();

    document.body.appendChild(a);
    a.click();
    a.remove();

    window.URL.revokeObjectURL(url);
}

async function createFolder() {

    const folderName =
        document.getElementById("folderName").value;

    if (!folderName) {
        return;
    }

    const path =
        `${currentPath}/${folderName}`;

    const response = await fetch(
        `/mkdir?path=${encodeURIComponent(path)}`,
        {
            method: "POST",
            headers: authHeaders()
        }
    );

    if (response.ok) {

        document.getElementById("folderName").value = "";

        loadFiles(currentPath);
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
}

loadMonitoring();
setInterval(
    loadMonitoring,
    10000
);
loadFiles();
loadDiskUsage();
