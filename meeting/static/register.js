$(document).ready(function () {
    let idCheck = false
    $('#idCheckBtn').on('click', function () {
        let id = $('#id').val()
        if (id == '' || id.trim().length == 0){
            alert('아이디를 입력해주세요')
        } else {
            $.ajax({
                type: 'POST',
                url: '/api/id_check',
                data: {
                    'id': id
                },
                success: function (data) {
                    console.log(data)
                    if (data.success) {
                        console.log(data.success)
                        idCheck = true
                    }
                }
            });
        }
    });

    $('#registerSubmit').on('click', function () {
        if (!idCheck) {
            alert('중복화인을 해주세요')
        } else {
            $('#registerForm').submit()
        }
    });
});