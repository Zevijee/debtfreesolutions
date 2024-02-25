var sipStack, callSession;

// Efficiently handle DOM content loaded
document.addEventListener('DOMContentLoaded', initSIPml5);

// Initialize SIPml5 with minimal changes for efficiency
function initSIPml5() {
    SIPml.init(() => {
        // Initialize SIP stack with necessary configuration
        sipStack = new SIPml.Stack({
            realm: 'geshmak.duckdns.org',
            impi: '1001',
            impu: 'sip:1001@geshmak.duckdns.org',
            password: 'pinny',
            websocket_proxy_url: 'wss://geshmak.duckdns.org:8089/ws',
            ice_servers: [{ urls: 'stun:stun.l.google.com:19302' }],
            events_listener: { events: '*', listener: onSipEventStack },
        });

        // Start the SIP stack with a callback for efficient event handling
        sipStack.start(e => {
            if (e.type === 'started') {
                // Log for successful start and proceed with registration
                console.log('SIP stack started successfully');
                register();
            } else {
                console.error('Failed to start the SIP stack:', e.description);
            }
        });

        console.log('SIPml5 initialization requested');
    }, e => console.error('Failed to initialize SIPml:', e));
}

// Registration and call handling with efficient event listeners
function register() {
    if (sipStack) {
        let registerSession = sipStack.newSession('register', {
            events_listener: { events: '*', listener: onSipEventSession }
        });
        registerSession.register();
    } else {
        console.error('SIP stack is not ready for registration.');
    }
}

function makeCall(phoneNumber) {
    if (sipStack) {
        let sipUri = `sip:${phoneNumber}@geshmak.duckdns.org`;
        callSession = sipStack.newSession('call-audio', {
            audio_remote: document.getElementById('audio_remote'),
            events_listener: { events: '*', listener: onSipEventSession },
            sip_caps: [
                { name: '+g.oma.sip-im', value: null },
                { name: 'language', value: '"en,fr"' }
            ]
        });
        callSession.call(sipUri);
    } else {
        console.error('SIP stack is not initialized, cannot make a call.');
    }
}

function hangUp() {
    if (callSession) {
        callSession.hangup();
    } else {
        console.error('No active call session to hang up.');
    }
}

// Global event listeners for efficient SIP event handling
function onSipEventStack(e) {
    console.log('onSipEventStack:', e.type, e);
    // Implement specific stack event handling logic here
}

function onSipEventSession(e) {
    console.log('onSipEventSession:', e.type, e);
    // Implement specific session event handling logic here
}
