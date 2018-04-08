$(function () {
    $("#search_name").autocomplete({
        source: "/passhint/autocomplete/",
        autoFocus: true
    });
});

$(function () {
    $('[data-toggle="popover"]').popover()
  })


function inline_pw_check(url, data, language)
{
    $.post(url, data)
    .done(function (response) {
        
        var content;
        var text;

        if(response.result == 'success')
        {
            if(language == 'ko')
            {
                text = '이 비밀번호는 사용가능합니다!';
            }
            else
            {
                text = 'You can use this password!';
            }

            content = '<div class="alert alert-success m-0 text-center" role="alert">'+ text +'</div>';
        }
        else if(response.result == 'warning')
        {
            if(language == 'ko')
            {
                text = '이 비밀번호는 아래 내용만 주의하면 사용가능합니다.';
            }
            else
            {
                text = 'You can use this Password. But becareful...';
            }
            content = '<div class="alert alert-warning m-0 text-center" role="alert">'+ text +'</div>';
            content += '<ul class="fa-ul m-2">';

            if(response.message['warning_en'] != "")
            {
                for (i = 0; i < response.message['warning_en'].length; i++)
                {
                    if(language == 'ko')
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['warning_ko'][i] + '</li>';
                    }
                    else
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['warning_en'][i] + '</li>';
                    }
                }
            }
        }
        else if(response.result == 'fail')
        {
            if(language == 'ko')
            {
                text = '이 비밀번호는 사용할 수 없습니다. 왜냐하면...';
            }
            else
            {
                text = 'You can not use this password. because...';
            }
            content = '<div class="alert alert-danger m-0 text-center" role="alert">'+ text +'</div>';
            content += '<ul class="fa-ul m-2">';

            if(response.message['error_en'] != "")
            {
                for (i = 0; i < response.message['error_en'].length; i++)
                {
                    if(language == 'ko')
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['error_ko'][i] + '</li>';
                    }
                    else
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['error_en'][i] + '</li>';
                    }
                }
            }

            if(response.message['warning_en'] != "")
            {
                for (i = 0; i < response.message['warning_en'].length; i++)
                {
                    if(language == 'ko')
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['warning_ko'][i] + '</li>';
                    }
                    else
                    {
                        content += '<li><i class="fa-li fa fa-check-square"></i>'+response.message['warning_en'][i] + '</li>';
                    }
                }
            }
        }
        else
        {
            alert('Please try again..');
        }
        
        $('#inline-pw-check-error').html(content);
    })
    .fail(function (xhr, textStatus, error) {
        alert('failed : ' + error);
    });
}