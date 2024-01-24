import { url } from './url.js';
const idInput = document.getElementById('idinput');
const passwordInput = document.getElementById('pwinput');
const signup = document.getElementById('signup');
const gotologin = document.getElementById('gotologin');

window.onload = function () {
    let wherefrom = localStorage.getItem('from');
    if (wherefrom == "failsignup") {
        var audio = new Audio('static/audio/signup/failsignup.mp3');
        audio.play();
    }
    if (wherefrom == "signup") {
        var audio = new Audio('static/audio/signup/signup.mp3');
        audio.play();
    }
    localStorage.removeItem('from');
};

signup.addEventListener('click', () => {
    let data = new FormData();
    data.append('id', idInput.value);
    data.append('password', passwordInput.value);

    fetch(url + '/signup', {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) { // 서버가 {success: True}를 보냈다면
                localStorage.setItem('token', data.token);
                localStorage.setItem('from', "sucsignup");
                window.location.href = "/main"; // 홈 화면으로 이동
            } else { // 서버가 {success: False}를 보냈다면
                alert("중복된 아이디입니다."); // 알림을 띄우고
                localStorage.setItem('from', "failsignup");
                window.location.href = "/signup"; // 로그인 화면으로 리다이렉트
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
})

gotologin.addEventListener('click', () => {
    localStorage.setItem('from', "login");
    window.location.href = "/login";
})