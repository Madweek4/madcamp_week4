import { url } from './url.js';
const idInput = document.getElementById('idinput');
const passwordInput = document.getElementById('pwinput');
const login = document.getElementById('login');
const gotosignup = document.getElementById('gotosignup');

window.onload = function () {
    let wherefrom = localStorage.getItem('from');
    if(wherefrom == "faillogin"){
        var audio = new Audio('static/audio/login/faillogin.mp3');
        audio.play();
    }
    if(wherefrom == "login"){
        var audio = new Audio('static/audio/login/login.mp3');
        audio.play();
    }
    localStorage.removeItem('from');
};

login.addEventListener('click', () => {
    let data = new FormData();
    data.append('id', idInput.value);
    data.append('password', passwordInput.value);

    fetch(url + '/login', {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) { // 서버가 {success: True}를 보냈다면
                localStorage.setItem('token', data.token);
                localStorage.setItem('from', "suclogin");
                window.location.href = "/main"; // 홈 화면으로 이동
            } else { // 서버가 {success: False}를 보냈다면
                alert("로그인에 실패했습니다."); // 알림을 띄우고
                localStorage.setItem('from', "faillogin");
                window.location.href = "/login"; // 로그인 화면으로 리다이렉트
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
})

gotosignup.addEventListener('click', () => {
    localStorage.setItem('from', "signup");
    window.location.href = "/signup";
})