// Wait for the entire HTML document to be loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('contactForm');
    const formStatus = document.getElementById('form-status');

    form.addEventListener('submit', async (e) => {
        // Prevent the default form submission behavior (which reloads the page)
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        formStatus.textContent = 'Sending...';
        formStatus.style.color = '#fcd34d'; // Amber 300

        try {
            const apiUrl = 'http://127.0.0.1:8000/contact';
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                formStatus.textContent = result.message;
                formStatus.style.color = '#22c55e'; // Green 500
                form.reset();
            } else {
                 const errorResult = await response.json();
                 formStatus.textContent = `Error: ${errorResult.detail || 'Could not send message.'}`;
                 formStatus.style.color = '#ef4444'; // Red 500
            }
        } catch (error) {
            formStatus.textContent = 'Could not connect to the server. Please try again later.';
            formStatus.style.color = '#ef4444'; // Red 500
            console.error('Fetch Error:', error);
        }
    });
});