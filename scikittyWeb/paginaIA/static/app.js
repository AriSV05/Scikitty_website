document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload');
    const contentDiv = document.getElementById('content');

    uploadButton.addEventListener('click', function() {
        // Limpiar el contenido actual del div
        contentDiv.innerHTML = '';

        // Crear un nuevo elemento para mostrar el nombre del archivo subido
        const fileNameElement = document.createElement('h3');
        fileNameElement.textContent = 'Nombre del archivo subido'; // Aquí puedes mostrar el nombre del archivo subido
        fileNameElement.classList.add('tituloArchivoSubido');
        contentDiv.appendChild(fileNameElement);

        const textArea = document.createElement('textarea');
        textArea.textContent = 'Nombre del archivo: ';
        textArea.classList.add('nombreArchivo')
        contentDiv.appendChild(textArea);

        // Crear botones "Metricas" y "ROC"
        const metricsButton = document.createElement('button');
        metricsButton.textContent = 'Metricas';
        metricsButton.className = 'buttonCargar';
        metricsButton.id = 'metricas';
        contentDiv.appendChild(metricsButton);

        const rocButton = document.createElement('button');
        rocButton.textContent = 'ROC';
        rocButton.className = 'buttonCargar';
        rocButton.id = 'roc';
        contentDiv.appendChild(rocButton);

        // Agregar listeners para los botones "Metricas" y "ROC"
        metricsButton.addEventListener('click', function() {
            // Lógica para el botón "Metricas"
        });

        rocButton.addEventListener('click', function() {
            // Lógica para el botón "ROC"
        });
    });
});
