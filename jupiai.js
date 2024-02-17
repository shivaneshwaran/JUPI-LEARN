const express = require('express');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/process_input', async (req, res) => {
    try {
        const user_input = req.body.user_input;
//AIzaSyDkYqYhYt3d6t63VgMJRgJby7bZJ5KViXc = apikey
        // Make a POST request to the Gemini API
        const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key=AIzaSyDkYqYhYt3d6t63VgMJRgJby7bZJ5KViXc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [
                    { role: 'user', parts: [{ text: user_input }] }
                ],
                generationConfig: {
                    temperature: 0.9,
                    topK: 1,
                    topP: 1,
                    maxOutputTokens: 2048,
                    stopSequences: []
                },
                safetySettings: [
                    { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
                    { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
                    { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
                    { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' }
                ]
            })
        });

        const data = await response.json();
        const model_response = data.contents.find(content => content.role === 'model').parts[0].text;

        res.json({ model_response });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
