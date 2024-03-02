var allData = []; 
var dataFetched = false; 

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded');

    configureDisplay();
    document.getElementById('zip-code-select').addEventListener('change', configureDisplay);

    configureSearch();
});

function configureDisplay() {
    const selectElement = document.getElementById('zip-code-select');
    const selectedZipCode = selectElement.value;
    const zipCodeElements = document.getElementsByClassName('zip-code');
    
    for (let i = 0; i < zipCodeElements.length; i++) {
        const zipCodeElement = zipCodeElements[i];
        
        if (zipCodeElement.id !== selectedZipCode) {
            zipCodeElement.style.display = 'none';
        } else {
            zipCodeElement.style.display = 'block';
        }
    }  
}

function configureSearch() {
    document.getElementById('searchPropertys').addEventListener('input', function() {
        var input = this.value.toLowerCase();
        var suggestions = document.getElementById('suggestions');
    
        function filterAndDisplaySuggestions(data) {
            var matches = Object.values(data).filter(item => item.address.toLowerCase().includes(input));
    
            suggestions.innerHTML = ''; // Clear previous suggestions
            if (matches.length > 0 && input.trim() !== '') {
                suggestions.style.display = 'block';
                matches.forEach(item => {
                    var div = document.createElement('div');
                    div.textContent = item.address;
                    // Apply styles to each suggestion div
                    div.style.padding = '10px';
                    div.style.margin = '1px 0';
                    div.style.background = '#f8f8f8';
                    div.style.cursor = 'pointer';

                    // Add hover effect
                    div.addEventListener('mouseover', function() {
                        div.style.background = '#eaeaea';
                    });

                    div.addEventListener('mouseout', function() {
                        div.style.background = '#f8f8f8';
                    });

                    div.addEventListener('click', function() {
                        window.location.href = '/property/' + item.id;
                        suggestions.style.display = 'none';
                    });
                    
                    div.style.padding = '10px';
                    div.style.margin = '1px 0';
                    div.style.background = '#f8f8f8';
                    div.style.cursor = 'pointer';
                    div.addEventListener('click', function() {
                        window.location.href = '/property/' + item.id;
                        suggestions.style.display = 'none';
                    });
                    suggestions.appendChild(div);
                });
            } else {
                suggestions.style.display = 'none';
            }
        }
    
        if (!dataFetched) {
            fetch('/return_properties')
                .then(response => response.json())
                .then(data => {
                    console.log('Data fetched:', data);
                    allData = data;
                    dataFetched = true;
                    filterAndDisplaySuggestions(allData);
                })
                .catch(error => console.error('Error fetching data:', error));
        } else {
            filterAndDisplaySuggestions(allData);
        }
    });

    
    // Event listener to show suggestions when the input is focused
    this.addEventListener('focus', function() {
        if (this.value.length > 0) {
            suggestions.style.display = 'block';
        }
    });

    // Event listener on the document to hide suggestions when clicking outside
    document.addEventListener('mousedown', function(event) {
        // Check if the clicked element is not the search bar and not a child of the suggestions div
        if (!this.contains(event.target) && !suggestions.contains(event.target)) {
            suggestions.style.display = 'none';
        }
    });    
}

