document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".form-container form");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent page reload

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (response.ok) {
                alert("Your service request has been submitted successfully!");
                form.reset();
            } else {
                alert("There was an error submitting your request. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An unexpected error occurred. Please try again.");
        }
    });
});