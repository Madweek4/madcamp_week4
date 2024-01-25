import { url } from '../url.js';

const name = document.getElementById('name');
const amount = document.getElementById('amount');
const donate = document.getElementById('donate');

var IMP = window.IMP;
IMP.init("imp42653145");

window.onload = function () {
    var audio = new Audio('static/audio/detail/detail.mp3');
    audio.play();
};

donate.addEventListener('click', () => {
    var audio = new Audio('static/audio/main/pay.mp3');
    audio.play();
    requestPay();
})

function requestPay() {
    IMP.request_pay(
        {
            pg: "TC0ONETIME",
            pay_method: "card",
            merchant_uid: name.value, //계속 변하는 값으로 수정 필요
            name: "BlindHelper-Donation",
            amount: amount.value,
            buyer_email: "Iamport@chai.finance",
            buyer_name: name.value,
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
                data.append('name', name.value);
                data.append('amount', amount.value);
                fetch(url + '/donate', {
                    method: 'POST',
                    body: data,
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) { // 서버가 {success: True}를 보냈다면
                            alert("기부를 완료했습니다."); // 알림을 띄우고
                            window.location.href = "/detail"; // 홈 화면으로 리다이렉트
                        } else { // 서버가 {success: False}를 보냈다면
                            alert("기부에 실패했습니다."); // 알림을 띄우고
                            window.location.href = "/detail"; // 홈 화면으로 리다이렉트
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

