document.addEventListener('DOMContentLoaded', async function () {
  const registers = document.getElementById('registers');

  // Clear previous results
  registers.innerHTML = "";

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

  // Retrieve data from the server and add data rows to the table
  const data = await overview(); // Wait for the data to be fetched

  // Freecodecamp :)
  function titleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return word.replace(word[0], word[0].toUpperCase());
    }).join(' ');
  }

  if (Array.isArray(data)) {
    data.forEach(function (result) {
      const row = document.createElement('tr');
      // TODO
      // Error - check keys of 'result'  -- Remake Route with correct joins
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
  } else {
    // Handle the case where data is not an array (e.g., an empty response)
    console.error('Invalid data received from the server.');
  }

  // Append the table to the searchResults element
  registers.innerHTML = '';
  registers.appendChild(table);

  async function overview() {
    let url = `/user/data`;

    const response = await fetch(url);
    const data = await response.json();

    return data;
  }
});
