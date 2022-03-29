$(document).ready(function () {
    $('#loginBtn').on('click', function () {
        let id = $('#id').val();
        let password = $('#password').val();
        if (id == '' || id.trim().length == 0 || password == '' || password.trim().length == 0) {
            alert('아이디와 비밀번호를 모두 입력해주세요')
        } else {
            $.ajax({
                type: 'POST',
                url: '/api/login',
                data: {
                    'id': id,
                    'password': password
                },
                success: function (data) {
                    if (data.success) {
                        $.cookie('myToken', data.token);
                        window.location.href = '/home';
                    } else {
                        alert(data.msg);
                    }
                }
            });
        }
    });
});