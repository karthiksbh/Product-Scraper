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
        list.innerHTML = '<li>Encountered an Error while trying to fetch the data. Please try again..</li>'; // Display error message
      });
  
    searchInput.value = '';
  });
  
  function displayResults(results) {
    const list = document.getElementById('list');
    list.innerHTML = '';
  
    results.forEach(function (transaction) {
      const listItem = document.createElement('li');
      listItem.innerHTML = `
        <h4>${transaction.title}</h4>
        <p>Platform: ${transaction.platform}</p>
        <p>Price: ${transaction.price}</p>
        <p>Ratings(Stars or %): ${transaction.rating}</p>
        <p>Reviews: ${transaction.review}</p>
        <br><a href="${transaction.url}" target="_blank" rel="noopener noreferrer">View Product</a>
      `;
  
      list.appendChild(listItem);
    });
  }
  