document.addEventListener('DOMContentLoaded', function() {
    configurePhoneCard();
});

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
    var phoneCards = document.getElementsByClassName('phone-details');
    console.log(phoneCards);

    for (var i = 0; i < phoneCards.length; i++) {
        phoneCards[i].onclick = function(event) {
            console.log(event);
            event.preventDefault();
            var phoneNumberId = this.id;
            showCustomDialog(phoneNumberId, this);           
        }
    }
}

function showCustomDialog(phoneNumberId, cardElement) {
    // Make an API call to the backend to the phone_number_config path
    fetch(`/phone_number_config/${phoneNumberId}`)
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            var number = data.number; // Assuming 'data' has a 'number' property
            var state = data.state; // Assuming 'data' has a 'state' property
            var realPhone = number.replace(/-/g, '').replace(/ /g, '').replace(/\(/g, '').replace(/\)/g, '');

            console.log(`realPhone: ${realPhone}`);

            // Now that we have the data, show the SweetAlert2 dialog
            Swal.fire({
                title: `Number: ${number}\nState: ${state}`,
                html: `
                    <select id="swal-input" class="swal2-input">
                        <option value="picked-up is the owner">Picked Up</option>
                        <option value="picked-up not the owner">Picked Up (Not Owner)</option>
                        <option value="declined">Declined</option>
                        <option value="busy">Busy</option>
                        <option value="ringing">Ringing</option>
                        <option value="voicemail">Voicemail</option>
                        <option value="Disconnected">Disconnected</option>
                        <option value="Unknown">Unknown</option>
                    </select>
                `,
                focusConfirm: false,
                preConfirm: () => {
                    return document.getElementById('swal-input').value;
                },
                
                didOpen: () => {
                    document.getElementById('call-button').addEventListener('click', () => makeCall(realPhone));
                }                
            }).then((result) => {
                if (result.isConfirmed) {
                    console.log('Result:', result)
                    // Do something with the result.value
                    updateNumberState(phoneNumberId, result.value);
                    stateElement = document.getElementById(`state${phoneNumberId}`);

                    stateElement.innerHTML = result.value;
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
