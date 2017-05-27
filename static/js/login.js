function login() {
    var password = $('#login_form #password').val();
    password = hex_md5(password)
    var dict = {
        'account': $('#reg_form #account').val(),
        'password': password,
    }
    $.post('/login', dict, function (data, ststus) {
        if (data == '0') {
            alert('用户名或密码错误');
        }
        else {
            location.href = '#'
        }
    });
    return false
}
function reg() {
    var password = $('#reg_form #password').val();
    if (password != $('#reg_form #c_password').val()) {
        alert('重复密码错误！')
        return false
    }
    password = hex_md5(password)
    var dict = {
        'account': $('#reg_form #account').val(),
        'password': password,
        'addr': $('#reg_form #addr').val(),
        'tel': $('#reg_form #phone').val()
    }
    $.post('/reg', dict, function (data, ststus) {
        if (data == '0') {
            alert('用户名重复');
        }
        else {
            location.href = '#'
        }
    });
    return false
}
$(document).ready(function () {
    /*
    $('#login_form').submit(function () {
        alert($('#login_form #account').val())
    });*/
});