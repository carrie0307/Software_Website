function add(id) {
    if (typeof ($.cookie('account')) == 'undefined') {
        location.href = '/login';
    };
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var flag = 0;
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart[i]['num']++;
            flag = 1;
        }
    }
    if (flag == 0) {
        cart[i] = { 'id': id, 'name': $('#name').text(), 'num': 1, 'price': $('[price]').attr('price') }
    }
    wrt_cart(cart);

};

function minus(id) {
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart[i]['num']--;
            if (cart[i]['num'] == 0) {
                cart.splice(i,1)
            }
        }
    }
    
    wrt_cart(cart);
};
function del(id) {
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart.splice(i, 1)
        }
    }

    wrt_cart(cart);

};

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]); return null;
}

function search() {
    location.href = '/search?word=' + $('#search_txt').text();
}

function ana_ids(st) {
    cart = [];
    var goods_list_temp = [];
    if (typeof (st) != 'undefined') {
        goods_list_temp = st.split(';');
    }
    for (var i = 0; i < goods_list_temp.length; i++) {
        info = goods_list_temp[i].split('&');
        cart[i] = { 'id': info[0], 'name': info[1], 'num': parseInt(info[2]), 'price': info[3] };
    };
    return cart
};

function wrt_cart(cart) {
    var st = '';
    var i = 0;
    for (var i = 0; i < cart.length; i++) {
        st = st + cart[i]['id'] + '&' + cart[i]['name'] + '&' + cart[i]['num'] + '&' + cart[i]['price'] + ';';
    }
    st = st.substring(0, st.length - 1);
    $.cookie('cart', st);
    $.cookie('cartlen', i);
}
function ini() {
    var account = $.cookie('account');
    var cartlen = $.cookie('cartlen');
    cart = $.cookie('cart');
    if (account) {
        $('#user').html('<i class="fa fa-user"></i> ' + account);
    }
    $('#cart').html('<i class="fa fa-heart-o"></i> Wishlist (' + cartlen + ') ');
}