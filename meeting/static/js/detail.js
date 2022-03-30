function likeBtn(_id) {
    var token = $.cookie('myToken')
    console.log(_id, token)
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

