document.addEventListener('DOMContentLoaded', function() {
    config();
});

function config() {
    // Updated WebSocket Interface and SIP credentials
    const socket = new JsSIP.WebSocketInterface('wss://debtfreesolutionsphone.duckdns.org:8089/ws');
    socket.via_transport = 'wss';

    // Updated Configuration with previous script's credentials
    const configuration = {
        uri: 'sip:1000@debtfreesolutionsphone.duckdns.org',
        password: 'pinny',
        realm: 'debtfreesolutionsphone.duckdns.org',
        register: true,
        session_timers: false,
        sockets: [socket]
    };

    const ua = new JsSIP.UA(configuration);

    // Setup events
    ua.on('connected', function () {
        console.log('Connected');
    });
    ua.on('disconnected', function () {
        console.log('Disconnected');
    });

    // Make a call
    const eventHandlers = {
        'progress': function (e) {
            console.log('call is in progress');
        },
        'failed': function (e) {
            // Show all call buttons
            const callButtons = document.getElementsByClassName('call-btn');

        },
        'ended': function (e) {
            console.log('call ended with cause: ' + (e.data ? e.data.cause : 'no cause'), e);
        },
        'confirmed': function (e) {
            console.log('call confirmed');
        },
        'addstream': (e) => {
            console.log('Add stream (event handlers)');
            audio.srcObject = e.stream;
            audio.play();
        }
    };

    const options = {
        'eventHandlers': eventHandlers,
        'mediaConstraints': {'audio': true, 'video': false}
    };

    const audio = new window.Audio();

    ua.on('registered', function () {
        console.log('Registered');
    });

    callListener = document.getElementsByClassName('call-btn');

    for (var i = 0; i < callListener.length; i++) {
        callListener[i].addEventListener('click', function() {
            var phoneNumber = this.dataset.number;
            makeCall(phoneNumber, this);
        });
    }

    makeCall = function (phoneNumber, callBtn) {
        callablePhoneNumber = phoneNumber.replace(/-/g, '').replace(/ /g, '').replace(/\(/g, '').replace(/\)/g, '');
        console.log(callablePhoneNumber);
        // Replace '0513887341' with the desired destination SIP URI
        const session = ua.call(`sip:${callablePhoneNumber}@debtfreesolutionsphone.duckdns.org`, options);
    
        if (session.connection) {
            console.log('Connection is valid');
    
            session.connection.addEventListener('addstream', e => {
                console.log('Add stream');
                audio.srcObject = e.stream;
                audio.play();
            });
        } else {
            console.log('Connection is null');
        }

        ua.on('newRTCSession', (data) => {
            console.log('New RTC Session');
            const session = data.session;
            session.on('addstream', function(e){
                // set remote audio stream (to listen to remote audio)
                // This method is modernized to avoid deprecated methods
                const remoteAudio = audio;
                remoteAudio.srcObject = e.stream;
                remoteAudio.play();
            });
        });
        ua.start();

        session.on('progress', function (e) {
            callBtn.style.display = 'none';

            console.log(`hangup-button${callBtn.id}`);

            var hangupBtn = document.getElementById(`hangup-button${callBtn.id}`);
            hangupBtn.style.display = 'block';

            const callButtons = document.getElementsByClassName('call-btn');
            for (let i = 0; i < callButtons.length; i++) {
                callButtons[i].style.display = 'none';
            }
                        
    ;
            hangupBtn.addEventListener('click', function() {
                callBtn.style.display = 'block'; 
                hangupBtn.style.display = 'none';

                for (let i = 0; i < callButtons.length; i++) {
                    callButtons[i].style.display = 'block';
                }
                
                session.terminate();
            });
        });

    }
    makeCall('00000000');
    hangupCall = function () {
        session.terminate();
    }
    hangupCall();
}