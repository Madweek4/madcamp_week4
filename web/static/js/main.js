import { url } from './url.js';

const token = localStorage.getItem('token');
const idDisplay = document.getElementById('id-display');
const payButton = document.getElementById('pay-button');
const demoButton = document.getElementById('demo-button')
const demoDisplay = document.getElementById('demo-display');
const helperDownload = document.getElementById('helper-download');
const licenseDownload = document.getElementById('license-download');
const demolicenseDownload = document.getElementById('demolicense-download');

var IMP = window.IMP;
IMP.init("imp42653145");

window.onload = function () {
    let wherefrom = localStorage.getItem('from');
    if (wherefrom == 'suclogin') {
        var audio = new Audio('static/audio/login/suclogin.mp3');
        audio.play();
    }
    if (wherefrom == 'sucsignup') {
        var audio = new Audio('static/audio/signup/sucsignup.mp3');
        audio.play();
    }
    if (wherefrom == 'sucpay') {
        var audio = new Audio('static/audio/signup/sucpay.mp3');
        audio.play();
    }

    let data = new FormData();
    data.append('token', token);

    fetch(url + '/main', {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) { // 서버가 {success: True}를 보냈다면
                if (data.user.ispaid) {
                    idDisplay.innerText = data.user.id + "님 환영합니다. 결제가 완료된 사용자입니다.";
                    helperDownload.style.display = 'inline-block';
                    licenseDownload.style.display = 'inline-block';
                }
                else {
                    idDisplay.innerText = data.user.id + "님 환영합니다.";
                    if (data.user.demo == "") {
                        payButton.style.display = 'inline-block';
                        demoButton.style.display = 'inline-block';
                    }
                    else {
                        helperDownload.style.display = 'inline-block';
                        demolicenseDownload.style.display = 'inline-block';
                        payButton.style.display = 'inline-block';
                        demoDisplay.style.display = 'inline-block';
                        demoDisplay.innerText = "demo version due date : " + data.user.demo;
                    }
                }

            } else { // 서버가 {success: False}를 보냈다면
                alert("유효하지 않은 토큰입니다."); // 알림을 띄우고
                window.location.href = "/login"; // 첫 화면으로 리다이렉트
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    localStorage.removeItem('from');
};


payButton.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/pay.mp3');
    audio.play();
    requestPay();
})

demoButton.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/demo.mp3');
    audio.play();
    let data = new FormData();
    data.append('token', token);

    fetch(url + '/demostart', {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) { // 서버가 {success: True}를 보냈다면
                alert("데모버전을 시작합니다"); // 알림을 띄우고
                window.location.href = "/main"; // 홈 화면으로 리다이렉트
            } else { // 서버가 {success: False}를 보냈다면
                alert("데모버전 시작 실패"); // 알림을 띄우고
                window.location.href = "/main"; // 홈 화면으로 리다이렉트
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
})

helperDownload.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/downzip.mp3');
    audio.play();
    window.location.href = "/download/blindhelper";
})

licenseDownload.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/downexe.mp3');
    audio.play();
    window.location.href = "/download/license";
})

demolicenseDownload.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/downexedemo.mp3');
    audio.play();
    window.location.href = "/download/demolicense";
})

function requestPay() {
    IMP.request_pay(
        {
            pg: "TC0ONETIME",
            pay_method: "card",
            merchant_uid: token,
            name: "BlindHelper",
            amount: 100000,
            buyer_email: "Iamport@chai.finance",
            buyer_name: "포트원 기술지원팀",
            buyer_tel: "010-1234-5678",
            buyer_addr: "서울특별시 강남구 삼성동",
            buyer_postcode: "123-456",
        },
        function (rsp) {
            // callback
            //rsp.imp_uid 값으로 결제 단건조회 API를 호출하여 결제결과를 판단합니다.
            if (rsp.success) {
                console.log(rsp);
                let data = new FormData();
                data.append('token', token);

                fetch(url + '/pay', {
                    method: 'POST',
                    body: data,
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) { // 서버가 {success: True}를 보냈다면
                            alert("결제를 완료했습니다."); // 알림을 띄우고
                            localStorage.setItem('from', "sucpay");
                            window.location.href = "/main"; // 홈 화면으로 리다이렉트
                        } else { // 서버가 {success: False}를 보냈다면
                            alert("결제에 실패했습니다."); // 알림을 띄우고
                            window.location.href = "/main"; // 홈 화면으로 리다이렉트
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            } else {
                console.log(rsp);
            }
        }
    );
}

