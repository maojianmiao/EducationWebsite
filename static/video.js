$(document).ready(function(){
	//INITIALIZE
	var video = $('#myVideo');

	//get base info
	
	courseid = findValue(document.URL, "courseid");
	videoid = findValue(document.URL,"videoid");

	//设置初始播放时间
	$.get('/video/record/get?' + "videoid=" + videoid,function(data,status){
		video[0].currentTime = Number(data);
	});
	//remove default control when JS loaded
	video[0].removeAttribute("controls");
	$('.control').show().css({'bottom':-45});
	$('.loading').fadeIn(500);
	$('.caption').fadeIn(500);
 
	//before everything get started
	video.on('loadedmetadata', function() {
		$('.caption').animate({'top':-45},300);
			
		//set video properties
		$('.current').text(timeFormat(0));
		$('.duration').text(timeFormat(video[0].duration));
		updateVolume(0, 0.7);
			
		//start to get video buffering data 
		setTimeout(startBuffer, 150);
			
		//bind video events
		$('.videoContainer')
		//.append('<div id="init"></div>')
		.hover(function() {
			$('.control').stop().animate({'bottom':0}, 500);
			$('.caption').stop().animate({'top':0}, 500);
		}, function() {
			if(!volumeDrag && !timeDrag){
				$('.control').stop().animate({'bottom':-45}, 500);
				$('.caption').stop().animate({'top':-45}, 500);
			}
		});
		
		$('.btnPlay').addClass('paused');
		video[0].play();
		//$('#init').fadeIn(200);
	});
	
	//display video buffering bar
	var startBuffer = function() {
		var currentBuffer = video[0].buffered.end(0);
		var maxduration = video[0].duration;
		var perc = 100 * currentBuffer / maxduration;
		$('.bufferBar').css('width',perc+'%');
			
		if(currentBuffer < maxduration) {
			setTimeout(startBuffer, 500);
		}
	};	
	
	//display current video play time
	video.on('timeupdate', function() {
		var currentPos = video[0].currentTime;
		var maxduration = video[0].duration;
		var perc = 100 * currentPos / maxduration;
		$('.timeBar').css('width',perc+'%');	
		$('.current').text(timeFormat(currentPos));	
	});
	
	//CONTROLS EVENTS
	//video screen and play button clicked
	video.on('click', function() { playpause(); } );
	$('.btnPlay').on('click', function() { playpause(); } );
	var playpause = function() {
		if(video[0].paused || video[0].ended) {
			$('.btnPlay').addClass('paused');
			video[0].play();
		}
		else {
			$('.btnPlay').removeClass('paused');
			video[0].pause();
		}
	};
	
	//speed text clicked
	$('.btnx1').on('click', function() { fastfowrd(this, 1); });
	$('.btnx2').on('click', function() { fastfowrd(this, 2); });
	$('.btnx4').on('click', function() { fastfowrd(this, 4); });
	var fastfowrd = function(obj, spd) {
		$('.text').removeClass('selected');
		$(obj).addClass('selected');
		video[0].playbackRate = spd;
		video[0].play();
	};
	
	//stop button clicked
	$('.btnStop').on('click', function() {
		$('.btnPlay').removeClass('paused');
		updatebar($('.progress').offset().left);
		video[0].pause();
	});
	
	//fullscreen button clicked
	$('.btnFS').on('click', function() {
		if($.isFunction(video[0].webkitEnterFullscreen)) {
			video[0].webkitEnterFullscreen();
		}	
		else if ($.isFunction(video[0].mozRequestFullScreen)) {
			video[0].mozRequestFullScreen();
		}
		else {
			alert('Your browsers doesn\'t support fullscreen');
		}
	});
	
	//light bulb button clicked
	$('.btnLight').click(function() {
		$(this).toggleClass('lighton');
		
		//if lightoff, create an overlay
		if(!$(this).hasClass('lighton')) {
			$('body').append('<div class="overlay"></div>');
			$('.overlay').css({
				'position':'absolute',
				'width':100+'%',
				'height':$(document).height(),
				'background':'#000',
				'opacity':0.9,
				'top':0,
				'left':0,
				'z-index':999
			});
			$('.videoContainer').css({
				'z-index':1000
			});
		}
		//if lighton, remove overlay
		else {
			$('.overlay').remove();
		}
	});
	
	//sound button clicked
	$('.sound').click(function() {
		video[0].muted = !video[0].muted;
		$(this).toggleClass('muted');
		if(video[0].muted) {
			$('.volumeBar').css('width',0);
		}
		else{
			$('.volumeBar').css('width', video[0].volume*100+'%');
		}
	});
	
	//VIDEO EVENTS
	//video canplay event
	video.on('canplay', function() {
		$('.loading').fadeOut(100);
	});
	
	//video canplaythrough event
	//solve Chrome cache issue
	var completeloaded = false;
	video.on('canplaythrough', function() {
		completeloaded = true;
	});
	
	//video ended event
	video.on('ended', function() {
		$('.btnPlay').removeClass('paused');
		video[0].pause();
	});

	//video seeking event
	video.on('seeking', function() {
		//if video fully loaded, ignore loading screen
		if(!completeloaded) { 
			$('.loading').fadeIn(200);
		}	
	});
	
	//video seeked event
	video.on('seeked', function() { });
	
	//video waiting for more data event
	video.on('waiting', function() {
		$('.loading').fadeIn(200);
	});
	
	//VIDEO PROGRESS BAR
	//when video timebar clicked
	var timeDrag = false;	/* check for drag event */
	$('.progress').on('mousedown', function(e) {
		timeDrag = true;
		updatebar(e.pageX);
	});
	$(document).on('mouseup', function(e) {
		if(timeDrag) {
			timeDrag = false;
			updatebar(e.pageX);
		}
	});
	$(document).on('mousemove', function(e) {
		if(timeDrag) {
			updatebar(e.pageX);
		}
	});
	var updatebar = function(x) {
		var progress = $('.progress');
		
		//calculate drag position
		//and update video currenttime
		//as well as progress bar
		var maxduration = video[0].duration;
		var position = x - progress.offset().left;
		var percentage = 100 * position / progress.width();
		if(percentage > 100) {
			percentage = 100;
		}
		if(percentage < 0) {
			percentage = 0;
		}
		$('.timeBar').css('width',percentage+'%');	
		video[0].currentTime = maxduration * percentage / 100;
	};

	//VOLUME BAR
	//volume bar event
	var volumeDrag = false;
	$('.volume').on('mousedown', function(e) {
		volumeDrag = true;
		video[0].muted = false;
		$('.sound').removeClass('muted');
		updateVolume(e.pageX);
	});
	$(document).on('mouseup', function(e) {
		if(volumeDrag) {
			volumeDrag = false;
			updateVolume(e.pageX);
		}
	});
	$(document).on('mousemove', function(e) {
		if(volumeDrag) {
			updateVolume(e.pageX);
		}
	});
	var updateVolume = function(x, vol) {
		var volume = $('.volume');
		var percentage;
		//if only volume have specificed
		//then direct update volume
		if(vol) {
			percentage = vol * 100;
		}
		else {
			var position = x - volume.offset().left;
			percentage = 100 * position / volume.width();
		}
		
		if(percentage > 100) {
			percentage = 100;
		}
		if(percentage < 0) {
			percentage = 0;
		}
		
		//update volume bar and video volume
		$('.volumeBar').css('width',percentage+'%');	
		video[0].volume = percentage / 100;
		
		//change sound icon based on volume
		if(video[0].volume == 0){
			$('.sound').removeClass('sound2').addClass('muted');
		}
		else if(video[0].volume > 0.5){
			$('.sound').removeClass('muted').addClass('sound2');
		}
		else{
			$('.sound').removeClass('muted').removeClass('sound2');
		}
	};

	//Time format converter - 00:00
	var timeFormat = function(seconds){
		var m = Math.floor(seconds/60)<10 ? "0"+Math.floor(seconds/60) : Math.floor(seconds/60);
		var s = Math.floor(seconds-(m*60))<10 ? "0"+Math.floor(seconds-(m*60)) : Math.floor(seconds-(m*60));
		return m+":"+s;
	};

	//###################videoplayer code as above########################################
	$(".navigator").on("click",function(){
			$(".navigator").removeClass('nselected');
			$(this).addClass("nselected");
		});

	$("#pageLast").on("click", function(){
			var className = $(this).attr("class");
			//控制class包含disabled的元素不能点击
			if (className.indexOf("disabled") > -1){
				return false;
			}
			var current = Number($(".pageSelected").text());
			console.log("current page: " + current);
			toPage = current - 1;
			courseid = findValue(document.URL, 'courseid');
			url = '/pages/' + toPage.toString() + "?" + "courseid=" + courseid;
			maxPage = Number($(".pagenum").last().text());

			$.get(url, function(data,status){
				$('.pbtn').removeClass('pageSelected')
				$("#commentUl").html(data);
				pageingRender(toPage, maxPage, "pagenum");
			});
		});

	$("#pageNext").on("click", function(){
			var className = $(this).attr("class");
			//控制class包含disabled的元素不能点击
			if (className.indexOf("disabled") > -1){
				return false;
			}
			var current = Number($(".pageSelected").text());
			console.log("current page: " + current);
			toPage = current + 1;
			courseid = findValue(document.URL, 'courseid');
			url = '/pages/' + toPage.toString() + "?" + "courseid=" + courseid;
			console.log(url);
			maxPage = Number($(".pagenum").last().text());

			$.get(url, function(data,status){
				$('.pbtn').removeClass('pageSelected')
				$("#commentUl").html(data);
				pageingRender(toPage, maxPage, "pagenum");
			});
		});

	$(".pagenum").on("click", function(){
			var className = $(this).attr("class");
			//控制class包含disabled的元素不能点击
			if (className.indexOf("disabled") > -1){
				return false;
			}
			var toPage = Number($(this).text());
			courseid = findValue(document.URL, 'courseid');
			url = '/pages/' + toPage.toString() + "?" + "courseid=" + courseid;
			maxPage = Number($(".pagenum").last().text());

			$.get(url, function(data,status){
				$('.pbtn').removeClass('pageSelected')
				$("#commentUl").html(data);
				pageingRender(toPage, maxPage, "pagenum");
				
			});
		});

	$(".pageout").on("click",function(){
		current_time = parseInt(video[0].currentTime);
		$.post("/video/record",{
			"current_time":current_time,
			"courseid":courseid,
			"videoid":videoid
		});
	});

});//document初始化结束标志

function showItem(id){
		var ids = new Array("commentArea","noteBox","detailBox");
		console.log("id is:" + id);
		elem = document.getElementById(id);
		elem.style= "";


		for (var item in ids){
			if (ids[item] != id){
				document.getElementById(ids[item]).style ="display:none";
			}
		}

}

//获取url中某个参数的值
function findValue(s, key){
	var value = s.match(key + "=" + "([^&#]*)");
	console.log(value);
	return value[1];

}

function addComment(){
	//textarea = document.getElementById("commentText").value;
	var pageRef = document.URL;
	console.log(pageRef);
	//获取课程id
	course_id = findValue(pageRef, 'courseid');
	video_id = findValue(pageRef, 'videoid');
	var textarea = $("#commentText").val(); //获取评论内容

	if (textarea.length<4){
		alert('最少输入4个字符！');
		return false;
	}
	var res = $.post('/add/comment',{
		courseid:course_id,
		videoid:video_id,
		comment:textarea,
	},
	function(data,textStatus){
		console.log(textStatus);
		if (textStatus == "success"){
			console.log(data);
			$("#commentText").val("");
			$("#commentCount").html(80);
			$("#commentUl").prepend(data);

		}
		else{
			return false;
		}
	});
}

function commentControl(wrods){
	var text = $(".inputCheck").val();
	if (text.length >= wrods){
		$("#commentCount").html(0);
		$("#commentCount").css({"color":"red"});
		var text = $(".inputCheck").val().substring(0,wrods);
		$(".inputCheck").val(text);
	}
	else{
		$("#commentCount").css({"color":"darkgreen"});
		valid = wrods - text.length;
		$("#commentCount").html(valid);
	}

}

function addNote(){
	var pageRef = document.URL;
	console.log(pageRef);
	//获取课程id
	course_id = findValue(pageRef, 'courseid');
	video_id = findValue(pageRef, 'videoid');
	var textarea = $("#noteText").val(); //获取笔记内容

	if (textarea.length<4){
		alert('最少输入4个字符！');
		return false;
	}
	var res = $.post('/add/note',{
		courseid:course_id,
		videoid:video_id,
		note:textarea,
	},
	function(data,textStatus){
		console.log(textStatus);
		if (textStatus == "success"){
			console.log(data);
			$("#noteText").val("");
			$("#noteUl").prepend(data);

		}
		else{
			return false;
		}
	});
}

//分页控制，输入当前页面和最大页面，输出一个长度为11的页面排列数组
function paging(cur, max){
	//例如：[1,...,13,14,15,16,17,18,19,20,21]
	var array = new Array()

	if (max<=11){
		for (i=0; i<max;i++){
			array[i] = i + 1;
		}
		return array;
	}
	
	array[0] = 1;
	array[10] = max;
	start = cur -3;
	if (cur - 5 > 1){
		//数组开始
		array[1] = '...';
	}
	else{
		array[1] =  2;
		start = 3;
	}

	if ( cur + 5 < max){
		array[9] = '...';
	}
	else{
		array[9] = max - 1;
		start = max - 8;
	}

	for (i=2; i<=8;i++){
		array[i] = start;
		start++;
	}

	return array;
}

function pageingRender(cur, max){
	elems = $(".pagenum");
	var array = paging(cur, max);
	console.log("array:  " + array);
	console.log(elems);
	console.log("cur: " + cur);
	$('.pbtn').removeClass('disabled');

	if (cur == 1){
		$("#pageLast").addClass("disabled");
	}
	if (cur == max){
		$("#pageNext").addClass("disabled");
	}
	for (var i in elems){
		elems[i].innerHTML = array[i];
		//console.log("set class name: " + array[i]);
		//console.log("cur: " + cur);

		if (array[i] == cur){
			elems[i].className = "pbtn pagenum pageSelected";
		}

		else if (array[i] == "..." ){
			console.log("... disabled");
			elems[i].className = "pbtn pagenum disabled";
		}
	}
	//复位滚动条
	document.getElementById("scrollControl").scrollTop = 0;
}