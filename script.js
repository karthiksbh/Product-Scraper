document.getElementById('form').addEventListener('submit', function (e) {
    e.preventDefault();
    const searchInput = document.getElementById('search');
    const query = searchInput.value;
    const list = document.getElementById('list');
    list.innerHTML = '<li>Loading...</li>'; // Display loading message
    
    fetch(`http://localhost:5000/search?query=${query}`)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        displayResults(data);
      })
      .catch(function (error) {
        console.error(error);
        list.innerHTML = '<li>Error occurred while fetching data</li>'; // Display error message
      });
  
    searchInput.value = '';
  });
  
  function displayResults(results) {
    const list = document.getElementById('list');
    list.innerHTML = '';
  
    results.forEach(function (transaction) {
      const listItem = document.createElement('li');
      listItem.innerHTML = `
        <h3>${transaction.title}</h3>
        <p>${transaction.platform}</p>
        <p>${transaction.price}</p>
        <a href="${transaction.url}" target="_blank" rel="noopener noreferrer">View Details</a>
      `;
  
      list.appendChild(listItem);
    });
  }
  