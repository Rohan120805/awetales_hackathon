document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const audioInput = document.getElementById('audio-input');
    const dropZone = document.getElementById('drop-zone');
    const uploadContent = dropZone.querySelector('.upload-content');
    const fileSelected = document.getElementById('file-selected');
    const fileName = document.getElementById('file-name');
    const removeFile = document.getElementById('remove-file');
    const languageSelect = document.getElementById('language-select');
    const ttsCheckbox = document.getElementById('tts-checkbox');
    const processBtn = document.getElementById('process-btn');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const englishOutput = document.getElementById('english-output');
    const translatedOutput = document.getElementById('translated-output');
    const audioOutputGroup = document.getElementById('audio-output-group');
    const audioOutput = document.getElementById('audio-output');
    const statusOutput = document.getElementById('status-output');
    const downloadTranscriptBtn = document.getElementById('download-transcript-btn');
    const transcriptFile = document.getElementById('transcript-file');

    let selectedFile = null;

    // File upload handling
    dropZone.addEventListener('click', () => audioInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type.startsWith('audio/')) {
            handleFileSelect(files[0]);
        }
    });

    audioInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        selectedFile = file;
        fileName.textContent = file.name;
        uploadContent.hidden = true;
        fileSelected.hidden = false;
        processBtn.disabled = false;
    }

    removeFile.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        audioInput.value = '';
        uploadContent.hidden = false;
        fileSelected.hidden = true;
        processBtn.disabled = true;
    });

    // Process audio
    processBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Reset outputs
        englishOutput.value = '';
        translatedOutput.value = '';
        audioOutputGroup.hidden = true;
        statusOutput.textContent = '';
        statusOutput.className = 'status-box';

        // Show progress
        progressContainer.hidden = false;
        processBtn.disabled = true;
        progressFill.style.width = '30%';
        progressText.textContent = 'Uploading and processing audio...';

        const formData = new FormData();
        formData.append('audio', selectedFile);
        formData.append('language', languageSelect.value);
        formData.append('tts', ttsCheckbox.checked ? 'true' : 'false');

        try {
            progressFill.style.width = '60%';
            progressText.textContent = 'Transcribing and translating...';

            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });

            progressFill.style.width = '90%';

            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }

            // Display results
            englishOutput.value = result.english_text || '';
            translatedOutput.value = result.translated_text || '';

            if (result.tts_audio) {
                audioOutput.src = `/api/audio/${result.tts_audio}`;
                audioOutputGroup.hidden = false;
            }

            statusOutput.textContent = result.tts_status || 'Processing complete!';
            statusOutput.className = 'status-box success';

            // Enable transcript download button
            downloadTranscriptBtn.disabled = false;

            progressFill.style.width = '100%';
            progressText.textContent = 'Complete!';

            setTimeout(() => {
                progressContainer.hidden = true;
                progressFill.style.width = '0%';
            }, 1500);

        } catch (error) {
            statusOutput.textContent = `Error: ${error.message}`;
            statusOutput.className = 'status-box error';
            progressContainer.hidden = true;
            progressFill.style.width = '0%';
        } finally {
            processBtn.disabled = false;
        }
    });

    // Download transcript
    downloadTranscriptBtn.addEventListener('click', async () => {
        const english = englishOutput.value;
        const translated = translatedOutput.value;
        const language = languageSelect.value;

        if (!english && !translated) return;

        try {
            const response = await fetch('/api/download/transcript', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    english: english,
                    translated: translated,
                    language: language
                })
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `transcript_${Date.now()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            statusOutput.textContent = 'Transcript downloaded!';
            statusOutput.className = 'status-box success';
        } catch (error) {
            statusOutput.textContent = `Download error: ${error.message}`;
            statusOutput.className = 'status-box error';
        }
    });

    // Upload transcript file directly
    transcriptFile.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        try {
            const text = await file.text();
            const lines = text.split('\n');

            let englishText = '';
            let translatedText = '';
            let section = '';

            for (const line of lines) {
                if (line.includes('English Transcription')) {
                    section = 'english';
                } else if (line.includes('Translation')) {
                    section = 'translated';
                } else if (line.trim() && !line.startsWith('===')) {
                    if (section === 'english') {
                        englishText += line + '\n';
                    } else if (section === 'translated') {
                        translatedText += line + '\n';
                    }
                }
            }

            englishOutput.value = englishText.trim();
            translatedOutput.value = translatedText.trim();

            // Reset file input
            transcriptFile.value = '';

            statusOutput.textContent = 'Transcript uploaded successfully!';
            statusOutput.className = 'status-box success';
            downloadTranscriptBtn.disabled = false;

        } catch (error) {
            statusOutput.textContent = `Upload error: ${error.message}`;
            statusOutput.className = 'status-box error';
        }
    });
});
