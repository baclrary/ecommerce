let files = [];

function validateFile(file) {
    if (file.size > 6 * 1024 * 1024) {
        alert(`File '${file.name}' is larger than 6MB. Please upload a smaller file or compress it.`);
        return false;
    }
    return true;
}

function updateFileList(input) {
    if (files.length + input.files.length > 10) {
        alert("You can only upload a maximum of 10 files");
        return;
    }

    for (let i = 0; i < input.files.length; i++) {
        if (validateFile(input.files[i])) {
            let duplicate = files.find(file => file.file.name === input.files[i].name && file.file.size === input.files[i].size && file.file.lastModified === input.files[i].lastModified);
            if (duplicate) {
                alert(`File '${input.files[i].name}' is already uploaded.`);
            } else {
                files.push({file: input.files[i], element: createFileElement(input.files[i], files.length)});
            }
        }
    }
    input.value = '';
    renderFileList();
}

function createFileElement(file, index) {
    const divItem = document.createElement('div');
    divItem.className = 'inline-block relative overflow-hidden text-center space-x-5 flex flex-col items-center justify-center';

    const removeButton = document.createElement('button');
    removeButton.textContent = 'x';
    removeButton.className = 'text-red-600 font-bold cursor-pointer mt-2 pr-5';

    removeButton.addEventListener('click', function () {
        removeFile(index);
    });

    // Helper function to get file extension
    function getFileExtension(fileName) {
        const parts = fileName.split('.');
        if (parts.length === 1 || (parts[0] === "" && parts.length === 2)) {
            return "";
        }
        return parts.pop().toLowerCase();
    }

    const fileExtension = getFileExtension(file.name);

    if (file.type.startsWith('image/') || ['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(fileExtension)) {
        const img = document.createElement('img');
        img.className = 'max-w-xxs max-h-xxs h-20 w-20 object-cover contain rounded';
        img.src = URL.createObjectURL(file);
        img.onload = function () {
            URL.revokeObjectURL(this.src);
        }
        divItem.appendChild(img);
    } else if (file.type.startsWith('video/') || ['mp4', 'avi', 'mkv'].includes(fileExtension)) {
        const video = document.createElement('video');
        video.className = 'max-w-xxs max-h-xxs h-20 w-20 object-cover contain rounded';
        video.controls = true;
        const source = document.createElement('source');
        source.type = file.type;
        source.src = URL.createObjectURL(file);
        video.appendChild(source);
        video.oncanplay = function () {
            URL.revokeObjectURL(this.src);
        }
        divItem.appendChild(video);
    } else {
        divItem.textContent += ' ' + file.name;
    }

    divItem.appendChild(removeButton);
    return divItem;
}

function removeFile(index) {
    const file = files.splice(index, 1)[0];
    file.element.parentNode.removeChild(file.element);
    renderFileList();
}

function renderFileList() {
    const uploadedFilesP = document.getElementById('uploadedFilesP');
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';

    if (files.length > 0) {
        uploadedFilesP.classList.remove('hidden');
        uploadedFilesP.textContent = `Uploaded files: ${files.length}`;

        if (files.length === 10) {
            uploadedFilesP.classList.add('text-red-600');
        } else {
            uploadedFilesP.classList.remove('text-red-600');
        }

        const container = document.createElement('div');
        container.className = 'inline-flex mx-auto flex-wrap space-x-5 bg-gray-50';

        for (const file of files) {
            container.appendChild(file.element);
        }
        fileList.appendChild(container);
    } else {
        uploadedFilesP.classList.add('hidden');
    }
}

document.getElementById('commentForm').addEventListener('submit', function (event) {
    event.preventDefault();
    if (files.length > 10) {
        alert("You can only upload a maximum of 10 files");
        return false;
    }
    const formData = new FormData(this);
    for (const file of files) {
        formData.append('media_files', file.file);
    }
    fetch(this.action, {
        method: this.method,
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
        .then(response => {
            // handle the response
            // document.getElementById('loadingModal').style.display = 'none';  // Hide the modal
            window.location.reload();
        })
        .catch(error => {
            // handle the error
            // document.getElementById('loadingModal').style.display = 'none';  // Hide the modal
        });
    document.getElementById('loadingModal').style.display = 'block';
});

