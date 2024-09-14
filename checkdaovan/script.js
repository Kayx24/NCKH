let fileList = [];

document.getElementById('files').addEventListener('change', function(event) {
    const files = Array.from(event.target.files);
    const tableBody = document.querySelector('#fileTable tbody');

    // Thêm các tệp mới vào fileList mà không làm mất các tệp cũ
    files.forEach(file => {
        if (!fileList.some(existingFile => existingFile.name === file.name)) {
            fileList.push(file);
            const row = tableBody.insertRow();
            const cell = row.insertCell(0);
            cell.textContent = file.name;
        }
    });
});

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Kiểm tra nếu không có file nào được chọn
    if (fileList.length === 0) {
        alert('Vui lòng chọn ít nhất một file.');
        return;
    }

    const formData = new FormData();
    fileList.forEach(file => {
        formData.append('files', file);
    });

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Mạng lỗi: Không thể tải dữ liệu.');
        }

        const result = await response.json();

        // Xây dựng bảng kết quả
        let resultText = '<h2>Ma trận tương đồng:</h2><table border="1"><thead><tr><th>File</th>';
        const files = Object.keys(result.matrix);
        files.forEach((file, index) => {
            resultText += `<th>File ${index + 1}</th>`;
        });
        resultText += '</tr></thead><tbody>';

        files.forEach((file1, i) => {
            resultText += `<tr><td>File ${i + 1}</td>`;
            files.forEach((file2) => {
                if (result.matrix[file1][file2]) {
                    const { verbatim, renaming, restructuring } = result.matrix[file1][file2];
                    resultText += `<td>Verbatim: ${verbatim.toFixed(2)}%, Renaming: ${renaming.toFixed(2)}%, Restructuring: ${restructuring.toFixed(2)}%</td>`;
                } else {
                    resultText += '<td>None</td>';
                }
            });
            resultText += '</tr>';
        });
        resultText += '</tbody></table>';
        
        document.getElementById('result').innerHTML = resultText;

    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu hoặc xử lý dữ liệu:', error);
        document.getElementById('result').innerHTML = 'Có lỗi xảy ra khi xử lý yêu cầu.';
    }

    // Không reset fileList hoặc bảng ở đây
});
