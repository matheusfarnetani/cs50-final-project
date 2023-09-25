document.addEventListener('DOMContentLoaded', async function () {
  const placeButtons = document.querySelectorAll('#place');
  const searchResults = document.getElementById('search-results');
  const elementsIds = ["card", "type", "date", "time", "place"];

  // Listen for input events
  elementsIds.forEach(function (elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.addEventListener('input', performSearch);
    }
  });

  // Add click event listeners to palce buttons
  placeButtons.forEach(function (placeButton) {
    placeButton.addEventListener('click', function () {
      const selectedPlace = placeButton.textContent === 'All' ? '' : placeButton.textContent;

      // Set the 'place' input value based on the button clicked
      document.getElementById('place').value = selectedPlace.toLowerCase();

      // Trigger the search
      performSearch();
    });
  });

  // Trigger an initial search without any filter parameters when the page is loaded
  await performSearch();

  // Freecodecamp :)
  function titleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return word.replace(word[0], word[0].toUpperCase());
    }).join(' ');
  }

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

    const response = await fetch('/api/tables?' + searchParams.toString());
    const data = await response.json();

    // Clear previous results
    searchResults.innerHTML = '';

    // Create a table and add header row
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `
            <th>Date</th>
            <th>Hour</th>
            <th>Minute</th>
            <th>Second</th>
            <th>Card Type</th>
            <th>Card UID</th>
            <th>Place</th>
            <th>Equipment</th>
        `;
    table.appendChild(headerRow);

    // Add data rows to the table
    data.forEach(function (result) {
      const row = document.createElement('tr');
      row.innerHTML = `
                <td>${result['date']}</td>
                <td>${result['hour']}</td>
                <td>${result['minute']}</td>
                <td>${result['second']}</td>
                <td>${titleCase(result['card type'])}</td>
                <td>${result['card uid']}</td>
                <td>${titleCase(result['place'])}</td>
                <td>${titleCase(result['equipment'])}</td>
            `;
      table.appendChild(row);
    });

    // Append the table to the searchResults element
    searchResults.innerHTML = '';
    searchResults.appendChild(table);
  }
});
