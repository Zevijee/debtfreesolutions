document.addEventListener('DOMContentLoaded', function() {
    configurePhoneCard();
    document.getElementById('call-btn').addEventListener('click', () => callQueque());
});

function callQueque() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const owners = document.getElementsByClassName('true-people')

    // get the owner that is currently visible
    for (var i = 0; i < owners.length; i++) {
        if (owners[i].style.display !== 'none') {
            owner = owners[i].id;
        }
    }

    fetch('/call', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            "mode": "queue",
            "owner": owner
        })
    })
}


function updateNumberState(phoneNumberId, newState) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/phone_number_config/${phoneNumberId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ state: newState })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
        // Optionally, inform the user about the error
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Something went wrong updating the phone number state!',
        });
    });
};


function configurePhoneCard() {
    var phoneCards = document.getElementsByClassName('phone-card');
    console.log(phoneCards);

    for (var i = 0; i < phoneCards.length; i++) {
        phoneCards[i].onclick = function(event) {
            console.log(event);
            event.preventDefault();
            var phoneNumberId = this.dataset.id;
            showCustomDialog(phoneNumberId, this);           
        }
    }
}

function makeACall(number) {
    // Make an API call to the backend to the phone_number_config path
    console.log('Making a call to: ' + number);
}


function showCustomDialog(phoneNumberId, cardElement) {
    // Make an API call to the backend to the phone_number_config path
    fetch(`/phone_number_config/${phoneNumberId}`)
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            var number = data.number; // Assuming 'data' has a 'number' property
            var state = data.state; // Assuming 'data' has a 'state' property

            // Now that we have the data, show the SweetAlert2 dialog
            Swal.fire({
                title: `Number: ${number}\nState: ${state}`,
                html: `
                    <button id="call-button">Call</button>
                    <br><br>
                    <select id="swal-input" class="swal2-input">
                        <option value="Active">Active</option>
                        <option value="Disconnected">Disconnected</option>
                        <option value="Unknown">Unknown</option>
                    </select>
                `,
                focusConfirm: false,
                preConfirm: () => {
                    return document.getElementById('swal-input').value;
                },
                didOpen: () => {
                    document.getElementById('call-button').addEventListener('click', () => makeACall(number));
                }                
            }).then((result) => {
                if (result.isConfirmed) {
                    console.log('Result:', result)
                    // Do something with the result.value
                    updateNumberState(phoneNumberId, result.value);
                    console.log(cardElement);
                    state = result.value;
                    cardElement.querySelector('h6').innerText = state;
                }
            });

        })
        .catch(error => {
            // Handle any errors
            console.error(error);
            // Optionally, inform the user about the error
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong fetching the phone number details!',
            });
        });
}
