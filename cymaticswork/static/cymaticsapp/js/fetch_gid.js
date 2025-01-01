// Assuming you have the SPREADSHEET_ID available
const SPREADSHEET_ID = '1HUq5i5pYUdzAwcOEKPlw2RkEe61yk0bc6lTvCI6nLAc'; // Replace with your actual Spreadsheet ID

function getGoogleSheetsUrl(sheetId) {
    // Form the Google Sheets URL
    return `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit#gid=${sheetId}`;
}

// Function to set the current URL and extract the GID
function setSheetUrlAndExtractGid(sheetId) {
    // Get the formed URL
    const googleSheetsUrl = getGoogleSheetsUrl(sheetId);

    // Use the formed Google Sheets URL directly to extract the GID
    const url = new URL(googleSheetsUrl); // Use the Google Sheets URL
    const gid = url.hash.split('gid=')[1] || null;

    if (gid) {
        console.log('Extracted GID:', gid);
        sendGidToBackend(gid); // Function to send the extracted GID to your backend
    } else {
        console.log('No GID found in the Google Sheets URL');
    }
}

function sendGidToBackend(gid) {
    fetch('/update-gid/', {  // Make sure this matches your Django view URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // Include CSRF token if using Django
        },
        body: JSON.stringify({ gid: gid })
    })
    .then(response => response.json())
    .then(data => {
        console.log('GID sent successfully:', data);
    })
    .catch(error => {
        console.error('Error sending GID:', error);
    });
}

function getCsrfToken() {
    // Function to get the CSRF token (if needed)
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Example usage with a specific sheet ID
setSheetUrlAndExtractGid(0); // Here '0' is an example sheetId. Replace with the actual sheetId you want to use.
