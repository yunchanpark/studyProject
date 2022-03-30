$(document).ready(function () {
    let token = $.cookie('myToken');
    if(token !== undefined) {
        token = JSON.parse(atob(token.split('.')[1]));
        $('#user_name').text(token.id + " 님")
    }
});

function logout() {
    $.removeCookie('myToken', {
        path: '/'
    });
    location.reload();
    window.location.href = '/home'
    alert('로그아웃 하셨습니다!')
}