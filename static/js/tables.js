document.addEventListener('DOMContentLoaded', async function () {
    const localButtons = document.querySelectorAll('#local');
    const searchResults = document.getElementById('search-results');
    const elementsIds = ["card", "type", "date", "time", "local"];

    // Listen for input events
    elementsIds.forEach(function (elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.addEventListener('input', performSearch);
        }
    });

    // Add click event listeners to local buttons
    localButtons.forEach(function (localButton) {
        localButton.addEventListener('click', function () {
            const selectedLocal = localButton.textContent === 'All' ? '' : localButton.textContent;

            // Set the 'local' input value based on the button clicked
            document.getElementById('local').value = selectedLocal;

            // Trigger the search
            performSearch();
        });
    });

    // Trigger an initial search without any filter parameters when the page is loaded
    await performSearch();

    async function performSearch() {
        const searchParams = new URLSearchParams();

        // Get search parameters from all form fields
        elementsIds.forEach(function (elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                // Exclude 'type' parameter if 'All' is selected
                if (!(elementId === 'type' && element.value === 'all')) {
                    searchParams.append(elementId, element.value);
                }
            }
        });

        const response = await fetch('/tables/search?' + searchParams.toString());
        const data = await response.json();

        // Clear previous results
        searchResults.innerHTML = '';

        // Create a table and add header row
        const table = document.createElement('table');
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `
            <th>Date</th>
            <th>Hours</th>
            <th>Minutes</th>
            <th>Seconds</th>
            <th>Card Type</th>
            <th>Card UID</th>
            <th>Equipment</th>
            <th>Local</th>
        `;
        table.appendChild(headerRow);

        // Add data rows to the table
        data.forEach(function (result) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${result['date']}</td>
                <td>${result['hours']}</td>
                <td>${result['minutes']}</td>
                <td>${result['seconds']}</td>
                <td>${result['card type']}</td>
                <td>${result['card uid']}</td>
                <td>${result['equipment']}</td>
                <td>${result['local']}</td>
            `;
            table.appendChild(row);
        });

        // Append the table to the searchResults element
        searchResults.innerHTML = '';
        searchResults.appendChild(table);
    }
});
