const login = document.getElementById('login');
const signup = document.getElementById('signup');
const detail = document.getElementById('detail');

window.onload = function () {
    localStorage.clear();
    document.body.classList.remove('is-preload');
};

window.ontouchmove = function() { return false; }
window.onorientationchange = function() { document.body.scrollTop = 0; }

login.addEventListener('click', () => {
    localStorage.setItem('from', "login");
    window.location.href = "/login";
})

signup.addEventListener('click', () => {
    localStorage.setItem('from', "signup");
    window.location.href = "/signup";
})

detail.addEventListener('click', () => {
    localStorage.setItem('from', "detail");
    window.location.href = "/detail";
})