let pc;
let localStream; // 本地媒体流

function createPeerConnection() {
    const configuration = {
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' } // 使用 Google STUN 服务器
        ]
    };

    const peerConnection = new RTCPeerConnection(configuration);

    // 处理 ICE 候选者
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            console.log('新 ICE 候选者: ', event.candidate);
            // 将候选者发送到远程对等方
        }
    };

    // 处理远程音频轨道
    peerConnection.ontrack = (event) => {
        const remoteAudio = document.getElementById('remoteAudio');
        if (remoteAudio.srcObject !== event.streams[0]) {
            remoteAudio.srcObject = event.streams[0];
        }
    };

    return peerConnection;
}

function negotiate() {
    pc.createOffer()
        .then((offer) => {
            return pc.setLocalDescription(offer);
        })
        .then(() => {
            // 将 offer 发送到远程对等方
            console.log('发送的 Offer: ', pc.localDescription);
        })
        .catch((error) => {
            console.error('协商过程中的错误: ', error);
        });
}

function start() {
    document.getElementById('start').style.display = 'none';

    pc = createPeerConnection();

    // 获取本地音频流
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            localStream = stream;

            // 将本地音频流添加到 PeerConnection
            localStream.getTracks().forEach((track) => {
                pc.addTrack(track, localStream);
            });

            // 执行 WebRTC 协商流程
            negotiate();
        })
        .catch((error) => {
            console.error('获取本地媒体流时出错: ', error);
        });

    document.getElementById('stop').style.display = 'inline-block';
}

// 事件监听器，用于启动连接
document.getElementById('start').onclick = start;