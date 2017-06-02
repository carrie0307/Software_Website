$(document).ready(function () {
    show('user');
});

function show(type) {
    var thead = '<thead><tr>'
    var todo = ''
    var dt=[]
    if (type == 'user') {
        //thead = thead + '<th>用户ID</th><th>用户名</th><th>地址</th><th>电话</th><th>操作</th>' + '</tr></thead><tbody></tbody>'
        $.get('/admin?type=user', function (data) {
            var j = 0
            for (var i in data['data']) {
                dt[j] = [];
                dt[j].push(i);
                dt[j].push(data['data'][i]['account']);
                dt[j].push(data['data'][i]['addr']);
                dt[j].push(data['data'][i]['tel']);
                
                dt[j].push('<a onclick="deluser(\'' + i + '\')">删除用户</a>')
                j++;
            }
            //$('#datatable1').html(thead);
            var t = $('#datatable1').dataTable({
                "data": dt,
                "sPaginationType": "full_numbers",
                "destroy":true,
                "pageLength": 20,
                "lengthMenu": [
                            [20, -1],
                            [20, "All"]
                ],

            });
            $('#d1').attr('class', 'row');
            $('#d2').attr('class', 'row hide');
            $('#d3').attr('class', 'row hide');
            
        });
        
    }
    else if (type == 'goods') {
        //thead = thead + '<th>商品ID</th><th>商品名</th><th>类型</th><th>价格</th><th>折扣</th><th>操作</th>' + '</tr></thead><tbody></tbody>'
        $.get('/admin?type=goods', function (data) {
            var j = 0
            for (var i in data['data']) {
                dt[j] = [];
                dt[j].push(i);
                dt[j].push(data['data'][i]['name']);
                dt[j].push(data['data'][i]['type']);
                dt[j].push(data['data'][i]['price']);
                dt[j].push(data['data'][i]['off']);
                dt[j].push('<a onclick="changeprice(\'' + i + '\')">改价格  </a><a onclick="changeoff(\'' + i + '\')">  改折扣</a>')
                j++;
            }
            //$('#datatable').html(thead);
            var t = $('#datatable2').dataTable({
                "data": dt,
                "sPaginationType": "full_numbers",
                "destroy": true,
                "pageLength": 20,
                "lengthMenu": [
                            [20, -1],
                            [20, "All"]
                ],

            });
            $('#d1').attr('class', 'row hide');
            $('#d2').attr('class', 'row');
            $('#d3').attr('class', 'row hide');
        });
    }
    else {
        //thead = thead + '<th>用户ID</th><th>商品ID</th><th>商品名</th><th>数量</th><th>总价</th><th>时间</th><th>状态</th><th>操作</th>' + '</tr></thead><tbody></tbody>'
        $.get('/admin?type=order', function (data) {
            var j = 0
            for (var i in data['data']) {
                dt[j] = [];
                dt[j].push(i);
                dt[j].push(data['data'][i]['uid']);
                dt[j].push(data['data'][i]['id']);
                dt[j].push(data['data'][i]['name']);
                dt[j].push(data['data'][i]['num']); 
                dt[j].push(data['data'][i]['sum']);
                dt[j].push(data['data'][i]['time']);
                dt[j].push(data['data'][i]['statue']);
                dt[j].push('<a onclick="delorder(\'' + i + '\')">删除订单</a>')
                j++;
            }
            //$('#datatable').html(thead);
            var t = $('#datatable3').dataTable({
                "data": dt,
                "sPaginationType": "full_numbers",
                "destroy": true,
                "pageLength": 20,
                "lengthMenu": [
                            [20, -1],
                            [20, "All"]
                ],

            });
            $('#d1').attr('class', 'row hide');
            $('#d2').attr('class', 'row hide');
            $('#d3').attr('class', 'row ');
        });
    }
    
};

function deluser(i) {
    dict={
        'type':'deluser',
        'id':i
    }
    $.post('/admin', dict, function () { show('user'); });
}
function changeprice(i) {
    price = prompt("请输入价格:");
    dict = {
        'type': 'changeprice',
        'id': i,
        'price':price
    }
    $.post('/admin', dict, function () { show('goods'); });
}
function changeoff(i) {
    off = prompt('请输入折扣:')
    dict = {
        'type': 'changeoff',
        'id': i,
        'off':off
    }
    $.post('/admin', dict, function () { show('goods'); });
}
function delorder(i) {
    dict = {
        'type': 'delorder',
        'id': i
    }
    $.post('/admin', dict, function () { show('order'); });
}