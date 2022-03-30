function likeBtn(_id) {
    var token = $.cookie('myToken')
    if (!token) {
        return
    }
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: {
            'postId_give': _id,
            'token': token
        },
        success: function (data) {
            if(data.result) {
                $('#likeBtn').val('좋아요 누른 상태')
            } else {
                $('#likeBtn').val('좋아요 안누른 상태')
            }
        }
    });
}

function join(_id) {
    var token = $.cookie('myToken')
    if (!token) {
        return
    }
    $.ajax({
        type: 'POST',
        url: '/api/join',
        data: {
            'postId_give': _id,
            'token': token
        },
        success: function (data) {
            if(data.people <= data.count) {
                $('#joinCk').val('인원마감')
                $('#joinCk').removeClass('btn-success')
                $('#joinCk').addClass('btn-secondary')
            } else {
                $('#joinCk').val('모집중')
                $('#joinCk').removeClass('btn-secondary')
                $('#joinCk').addClass('btn-success')
            }

            if (data.result) {
                $('#join').val('참여하기 누른 상태')
            } else {
                $('#join').val('참여하기 안누른 상태')
            }
        }
    });
}

