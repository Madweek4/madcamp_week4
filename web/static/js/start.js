const login = document.getElementById('login');
const signup = document.getElementById('signup');

window.onload = function () {
    localStorage.clear();
};

login.addEventListener('click', () => {
    localStorage.setItem('from', "login");
    window.location.href = "/login";
})

signup.addEventListener('click', () => {
    localStorage.setItem('from', "signup");
    window.location.href = "/signup";
})