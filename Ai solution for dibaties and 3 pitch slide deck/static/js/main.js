/**
 * DiabetesPredict - Main JavaScript functionality
 */

// Function to generate random prediction data
function generateRandomPrediction() {
    const glucose = Math.floor(Math.random() * 200) + 70;
    const bmi = (Math.random() * 20 + 18).toFixed(1);
    const age = Math.floor(Math.random() * 50) + 20;
    const probability = Math.random();

    return {
        glucose,
        bmi,
        age,
        prediction: probability > 0.5 ? 1 : 0,
        probability: (probability * 100).toFixed(1)
    };
}

// Function to update the prediction display
function updatePredictionDisplay() {
    const data = generateRandomPrediction();
    const predictionElement = document.querySelector('.prediction-result');

    if (predictionElement) {
        const riskLevel = data.probability > 70 ? 'High' : data.probability > 30 ? 'Medium' : 'Low';
        const riskClass = data.probability > 70 ? 'danger' : data.probability > 30 ? 'warning' : 'success';

        predictionElement.innerHTML = `
            <div class="alert alert-${riskClass} mb-4">
                <h4 class="alert-heading">Risk Level: ${riskLevel}</h4>
                <p class="mb-0">Probability: ${data.probability}%</p>
            </div>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Key Metrics</h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Glucose: ${data.glucose} mg/dL</li>
                        <li class="list-group-item">BMI: ${data.bmi}</li>
                        <li class="list-group-item">Age: ${data.age} years</li>
                    </ul>
                </div>
            </div>
        `;
    }
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form validation for the prediction form
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', validateForm);
    }

    // Initialize any tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add event listeners to numeric inputs to validate input
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNumericInput(this);
        });
    });

    // Initialize prediction display when page loads
    const predictionElement = document.querySelector('.prediction-result');
    if (predictionElement) {
        updatePredictionDisplay();
    }
});

/**
 * Validates the prediction form before submission
 * @param {Event} event - The form submission event
 */
function validateForm(event) {
    let isValid = true;
    const form = event.target;

    // Get all required inputs
    const requiredInputs = form.querySelectorAll('input[required]');

    // Check each required input
    requiredInputs.forEach(input => {
        // Clear previous validation state
        input.classList.remove('is-invalid');

        // Check if empty
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
            return;
        }

        // For number inputs, check if it's within min-max range
        if (input.type === 'number') {
            const value = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            if (isNaN(value) || value < min || value > max) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        }
    });

    // If not valid, prevent form submission
    if (!isValid) {
        event.preventDefault();
        showValidationAlert();
    }
}

/**
 * Validates a numeric input for range constraints
 * @param {HTMLElement} input - The input element to validate
 */
function validateNumericInput(input) {
    // Remove invalid class to start fresh
    input.classList.remove('is-invalid');

    // If empty, don't validate yet (will be caught on submission)
    if (!input.value.trim()) return;

    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);

    // Check if the number is valid and within range
    if (isNaN(value) || value < min || value > max) {
        input.classList.add('is-invalid');
    }
}

/**
 * Shows an alert for form validation errors
 */
function showValidationAlert() {
    // Check if an alert already exists
    const existingAlert = document.querySelector('.validation-alert');
    if (existingAlert) return;

    // Create alert element
    const alertElement = document.createElement('div');
    alertElement.className = 'alert alert-danger alert-dismissible fade show validation-alert';
    alertElement.role = 'alert';
    alertElement.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        Please fill in all required fields with valid values.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Insert at the top of the form
    const form = document.getElementById('predictionForm');
    form.parentNode.insertBefore(alertElement, form);

    // Scroll to the alert
    alertElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Automatically dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertElement);
        bsAlert.close();
    }, 5000);
}

/**
 * Handles copying content to clipboard
 * @param {string} text - The text to copy
 * @param {HTMLElement} button - The button element that triggered the copy
 */
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        // Store original button text
        const originalText = button.innerHTML;

        // Change button text to indicate success
        button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';

        // Restore original text after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}

/**
 * Display a toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of toast (success, warning, danger, info)
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Create a unique ID for the toast
    const toastId = 'toast-' + Date.now();

    // Create toast HTML
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">DiabetesPredict</strong>
                <small class="text-white">Educational Tool Only</small>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
                <div class="small text-muted mt-1">This tool is for educational purposes only and should not replace professional medical advice.</div>
            </div>
        </div>
    `;

    // Add toast to container
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);

    // Initialize and show the toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();

    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}