document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const image = document.getElementById('image').files[0];
    const gender = document.getElementById('gender').value;

    const formData = new FormData();
    formData.append('image', image);
    formData.append('gender', gender);

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    document.getElementById('loading').classList.add('hidden');
    document.getElementById('results').classList.remove('hidden');

    document.getElementById('tone').innerText = data.skin_tone;
    document.getElementById('rgb').innerText = data.rgb.join(', ');
    document.getElementById('recommendation').innerText = data.recommendation;
});