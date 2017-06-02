$(document).ready(function () {

    var len, data
    //首页信息
    $.get('/off', function (data1, ststus) {
        len = data1['length'];
        data = data1['data'];
        
    
    //len = 6; 
    //data = { '0101': ['AIPC笔记本电脑', 600, 75], '0102': ['小米√3', 600, 75], '0103': ['锁尼兰牙耳机', 600, 75], '0104': ['基械键盘', 600, 75], '0105': ['金是顿U盘', 600, 75], '0106': ['平果MP3', 600, 75] };
		var ins = $('#product-slide').find(".carousel-inner")
		var flag = 0
		for (var i in data) {
		    var a = '';
		    if (flag == 0) {
		        a = ' active';
		        flag++;
		    }
		    var str = '<div class="item' + a + '"><div class="container"><div class="row"><div class="col-sm-7"><div class="intro-content"><h1>'+
		        data[i][0] + '</h1><h2>现价<span class="highlight">￥' + (data[i][1] * (100-data[i][2])/100) +
		        '</span></h2><a class="btn btn-default" href="/detail?id='+i+'">Prechase Now</a></div></div><div class="col-sm-5"><div class="intro-content"><img class="img-responsive" src="static/images/goods/' +
		        i + '.jpg" alt="" /></div>	</div>	</div>	</div>	</div>';
		    ins.append(str);
		}
    });

    //自动登录

    //var uid = $.cookie('uid');
    ini();

});
