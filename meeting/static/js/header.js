$(document).ready(function () {
    let token = $.cookie('myToken');
    if (token !== undefined) {
        token = JSON.parse(atob(token.split('.')[1]));
        $('#user_name').text(token.name + " 님")
    }
});

function logout() {
    $.removeCookie('myToken', {
        path: '/'
    });
    location.reload();
    window.location.href = '/'
    alert('로그아웃 하셨습니다!')
}

function goMain() {
    location.replace("/")
}