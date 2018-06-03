var imgs = [
	{{links}}
];
imgs.sort(function() {
    return .5 - Math.random();
});
//单例模式
var loadimg = (function(){
	var oBox = document.getElementById('box'),
		pageCount = 10,//假设每页10个图片
	    ind = 0, //累加器---分页，每页10个图片
	    total;

	return {
		//加载图片
		load:function(){
			var oImg = new Image();//创建oImg
			var img = imgs[ind%imgs.length];
			oImg.src = img.src; //设置图片路径
			oImg.style.opacity = '0';
			this.shortLi().appendChild(oImg);
			setTimeout(function(){
				oImg.style.opacity = '1';
				oImg = null;//清除oImg
			},1);			
			
		},
		//计算哪一个li高度最小
		shortLi:function(){
			var oUl  = oBox.children[0],
			    oLi  = oUl.children,
	            minH = Infinity,//无限高
	            curLi;
	        	for(var i=0;i<oLi.length;i++){
					if(oLi[i].offsetHeight < minH){
						minH = oLi[i].offsetHeight;
						curLi = oLi[i];
					}
			    }
			    return curLi;	
		},
		//
		autoload:function(){
			if(ind<pageCount){
				for(;ind<pageCount;ind++){
					this.load();
				}
			}else{
				total = ind;
				for(;ind<total+1;ind++){
					this.load();
				}
			}
		}
	}
})();
//第一次加载(加载第一页)
loadimg.autoload();
//滚动加载
window.onscroll = function(){
	var bot = document.getElementById('bot'),
		botT = bot.offsetTop,
	    sH = document.documentElement.clientHeight, //浏览器可视高度
	    docH = document.body.clientHeight, //文档内容高度
	    scrH = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop; //滚动高度(兼容性问题)
	if(scrH+sH >= botT){
		loadimg.autoload();
	}
}
