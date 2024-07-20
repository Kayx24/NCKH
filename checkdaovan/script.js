let fileList = [];

document.getElementById('files').addEventListener('change', function(event) {
    const files = event.target.files;
    const tableBody = document.querySelector('#fileTable tbody');

    for (let i = 0; i < files.length; i++) {
        fileList.push(files[i]);
    }

    tableBody.innerHTML = '';

    fileList.forEach((file, index) => {
        const row = tableBody.insertRow();
        const cell = row.insertCell(0);
        cell.textContent = file.name;
    });
});

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();

    fileList.forEach(file => {
        formData.append('files', file);
    });

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    let resultText = 'Similarity Matrix:<br>';
    result.matrix.forEach((row, i) => {
        resultText += `<strong>File ${i + 1}</strong>: ${row.map((similarity, j) => `File ${j + 1}: ${similarity.toFixed(2)}%`).join(', ')}<br>`;
    });
    document.getElementById('result').innerHTML = resultText;

    // Reset fileList and clear the table
    fileList = [];
    document.querySelector('#fileTable tbody').innerHTML = '';
});
