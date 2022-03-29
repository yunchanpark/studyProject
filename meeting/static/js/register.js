$(document).ready(function () {
    let idCheck = false;
    $('#idCheckBtn').on('click', function () {
        let id = $('#id').val();
        if (id == '' || id.trim().length == 0){
            alert('아이디를 입력해주세요');
        } else {
            $.ajax({
                type: 'POST',
                url: '/api/id_check',
                data: {
                    'id': id
                },
                success: function (data) {
                    if (data.success) {
                        idCheck = true;
                        alert("생성 가능한 ID 입니다")
                    }
                    else {
                        alert("중복된 ID 입니다")
                    }
                }
            });
        }
    });

    $('#registerSubmit').on('click', function () {
        if (!idCheck) {
            alert('중복화인을 해주세요');
        } else {
            let registerForm = $('form[name=registerForm]').serialize();
            $.ajax({
                type: 'post',
                url: 'api/register',
                dataType: 'json',
                data: registerForm,
                success: function(data) {
                    if(data.success) {
                        alert(data.msg)
                        window.location.href = '/login'
                    }
                }
            })
        }
    });
});