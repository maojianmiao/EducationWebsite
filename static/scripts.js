$(document).ready(function(){

  root_url = document.URL
  if (root_url.indexOf('?') > -1){
    root_url = root_url.slice(0, root_url.indexOf('?'));
  }

  root_url = root_url.replace('#','');
  var toPage;
  maxPage = Number($(".pagenum").last().text());
  $("#pageLast").on("click", function(){
      var className = $(this).attr("class");
      //控制class包含disabled的元素不能点击
      if (className.indexOf("disabled") > -1){
        return false;
      }
      var current = Number($(".pageSelected").text());
      console.log("current page: " + current);
      toPage = current - 1;
      url = root_url + '?pid=' + toPage;
      window.location = url;
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

      //页面地址
      url = root_url + '?pid=' + toPage;
      console.log(url);

      window.location = url;
    });

  $(".pagenum").on("click", function(){
      var className = $(this).attr("class");
      //控制class包含disabled的元素不能点击
      if (className.indexOf("disabled") > -1){
        return false;
      }
      var toPage = Number($(this).text());
      //页面地址
      url = root_url + '?pid=' + toPage;

      window.location = url;
    });
    //通用分页渲染
    if (document.URL.indexOf('pid')> -1){
        toPage = Number(getParamValue('pid'));
    
    }
    pageingRender(toPage, maxPage);

    //渲染用户查看课程记录页面
    renderRecord();

    $('.btn_add_collect').click(function(){
      course_id = $('.course_info').attr('course_id');
      console.log(course_id);
      if ($(this).attr('class').indexOf('added') > -1){
        $.post('/course/collect/cancel',{
            course_id:course_id,
          },
        function(data, status){
            console.log(data + status);
            $('.btn_add_collect').text('添加收藏');
            $('.btn_add_collect').removeClass('added');
        });}
      
      else{
          $.post('/course/collect/add',{
            course_id:course_id,
          },
          function(data, status){
              console.log('add: ' + data + status);
              $('.btn_add_collect').html('已收藏');
              $('.btn_add_collect').addClass('added');
          });}
    });
    //渲染导航“所有课程”的下拉菜单
    $.get("/menu",function(data,status){
        $(".ac_menu").html(data);
    });


     
    $('.all_check').click(function(){
      elems = $('.single_check')
      if (this.checked == true){
        for (var i in elems){
          elems[i].checked = true;
        }
      }
      else{
        for (var i in elems){
          elems[i].checked = false;
        }
      }});

    $('.m_edit').click(function(){
        var elems = $('.single_check:checked');
        if (elems.length>1){
          alert("一次只能编辑一个项目");
          return false;
        }
        if (elems.length==0){
          alert("请选择一个要编辑的项目");
          return false;
        }
        $('.for_close').css('z-index','999');
        $.get('/course/edit?course_id=' + elems[0].value,function(data, status){
          if (status == "success"){
            $('.for_close').html(data);
          }
        });
    });

    $('.v_edit').click(function(){
        var elems = $('.single_check:checked');
        if (elems.length>1){
          alert("一次只能编辑一个项目");
          return false;
        }
        if (elems.length==0){
          alert("请选择一个要编辑的项目");
          return false;
        }
        $('.for_close').css('z-index','999');
        $.get('/lesson/edit?vid=' + elems[0].value,function(data, status){
          if (status == "success"){
            $('.for_close').html(data);
          }
        });
    });

    //用户搜索时根据输入的字符，动态推荐一些课程
    $('#search_text').keyup(function(){
      text = $(this).val();
      if (!text){
          $('.search_help').html('');
          console.log('空字符串');
          return false;
      }

      $.get('/input/refer?text=' + text,function(data,status){
        if (status=='success' && data){
          $('.search_help').html(data);//找到class为search_help的元素，把data填充到此元素下
        }
        else{
          $('.search_help').html('');
        }
      });
    });

    clearLabel();
}); // end of document


function getXmlhttp(){
  if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
    }
  else
    {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

function validateEmail(id)
{

  value = document.getElementById(id).value

  if (!value){
    return "邮箱不能为空";
  }
    apos=value.indexOf("@");
    dotpos=value.lastIndexOf(".");
    if (apos<1||dotpos-apos<2) 
    {
      return "请输入正确的邮箱地址"
    }
  else 
    /* 验证通过，返回空字符串*/
    {return "";}

}

function validateInfo()
{

  value = document.getElementById("infoTextarea").innerHTML;

    if (value>100) 
    {
      document.getElementById("infoMessageBox").innerHTML="简介不能超过100个字符！"
      return false;
    }
  else 
    /* 验证通过，返回空字符串*/
  document.getElementById("infoMessageBox").innerHTML=""
    {return true;}
}

/*验证昵称是否合法，不能为空，不能超过22个字符*/
function validateNickname(str){
  if (!str){
    document.getElementById("nickMessageBox").innerHTML = '昵称不能为空!'
    return false
  }
  if (str.length>22){
    document.getElementById("nickMessageBox").innerHTML = '昵称不能超过22个字符！'
    return false
  }
  document.getElementById("nickMessageBox").innerHTML = '';
  return true;
}
/*验证手机号是否合法*/
function validatePhone(str){
          if (!str){
            document.getElementById('phoneMessageBox').innerHTML = '';
            return true;
          }
          var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;  
          if (!myreg.test(str)) { 
              document.getElementById('phoneMessageBox').innerHTML = '请输入有效的手机号码！';
              return false;  
          } else {  
            document.getElementById('phoneMessageBox').innerHTML = '';
            return true;  
          }  
}

/*验证qq号是否合法*/
function validateQQ(str){
        if (!str){
          document.getElementById('qqMessageBox').innerHTML = '';
          return true;
        }
          var myreg=/[1-9][0-9]{4,}/;  
          if (!myreg.test(str)) { 
              document.getElementById('qqMessageBox').innerHTML = '请输入有效的QQ号码！'
              return false;  
          } else {  
              document.getElementById('qqMessageBox').innerHTML = '';
              return true;  
          }  
}

/*验证微信号是否合法*/
function validateWechat(str){
        if (!str){
          document.getElementById("wechatMessageBox").innerHTML="";
          return true;
        }
        if (str.length>30){
          document.getElementById("wechatMessageBox").innerHTML="请输入合法的微信号！";
          return false
        }
        else{
          document.getElementById("wechatMessageBox").innerHTML="";
          return true
        }
}


function getAuthCode(id)
{
  console.log('get auth code');
  document.getElementById('login_input_note').innerHTML = "";
  $('.input_note').removeClass('warning_note');
  msg = validateEmail('username');
  /*倒计时的时候不可点击*/
  if (document.getElementById(id).innerHTML.lastIndexOf("秒") > -1){ 
    console.log("false");
    return false;
  }
  //验证邮箱输入
  if (msg){
    document.getElementById('login_input_note').innerHTML = msg
    $('.input_note').addClass('warning_note');
    return false
  }
  var str = document.getElementById("username").value;
  confirmSign = checkEmail(str);
  console.log(confirmSign);

  
  if (!confirmSign){
      document.getElementById('login_input_note').innerHTML = "此邮箱已被注册！";
      $('.input_note').addClass('warning_note');
      return false;
  }


  xmlhttp = getXmlhttp();

  xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    count(60,id);
    
    }
  }
    xmlhttp.open("GET","/auth_code?username="+str,true);
    xmlhttp.send();
}

function count(time,id){
    if (time == 0){
        document.getElementById(id).innerHTML="获取验证码"
        $('#btn_auth_code').css('background-color','olive');
        return true
    }
    document.getElementById(id).innerHTML = time + '秒';
    time = time - 1;
    // 拼一个javascript字符串，类似：count(time,id)
    script = "count(" + time + "," + "'" + id + "'" + ")"
    //递归
    $("#btn_auth_code").css('background-color','gray');
    t = setTimeout(script,1000);
    
}

function uploadFile(id){
  var elem = document.getElementById(id)
  elem.click()
  elem.onchange=function(){
    console.log("2inputting!!");
    _upload(id,"/upload/images");
  }
}

function uploadVideo(id){
  var elem = document.getElementById(id)
  elem.click()
  elem.onchange=function(){
    //_upload(id,"/new/upload");
    _upload_ajax(id,"/new/upload");
  }
}
function _upload(id, url){

  var form = document.getElementById('upload');
  formData = new FormData(form); 
  var xmlhttp = getXmlhttp();

  formData.append("uplaod",1);
  formData.append(id, document.getElementById(id).files[0]);
  
  xmlhttp.onreadystatechange=function()
    {
     if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
         console.log("xmlhttp.responseText");
        console.log(xmlhttp.responseText);
        imgElem = document.getElementById("headImg");
        imgElem.src = xmlhttp.responseText;
      }
    }
  xmlhttp.open("post",url,true);
  xmlhttp.send(formData);
  }

function _upload_ajax(id,url){
  var form = document.getElementById('upload');
  formData = new FormData(form); 
  var xmlhttp = getXmlhttp();

  formData.append("uplaod",1);
  formData.append(id, document.getElementById(id).files[0]);
  xmlhttp.upload.onprogress=function(e){
    onprogress(e);
  }

  xmlhttp.onreadystatechange=function()
    {
     if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
         console.log("xmlhttp.responseText");
        console.log(xmlhttp.responseText);
        imgElem = document.getElementById("headImg");
        imgElem.src = xmlhttp.responseText;
      }
    }
  xmlhttp.open("post",url,true);
  xmlhttp.send(formData);

}

function onprogress(evt){
     var loaded = evt.loaded;   //已经上传大小情况 
     var tot = evt.total;   //附件总大小 
     var per = Math.floor(100*loaded/tot); //已经上传的百分比 
     $(".progress_text").text("进度："+ per +"%");
};
function onChangeControl(labelid){

    value = document.getElementById("infoTextarea").innerHTML;
    console.log(value);
    if (value){
    elem = document.getElementById(labelid);
    elem.style = "display:none";
  }
}

function settingReq(){
   if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
    }
  else
    {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    var obj = new Object();
    obj.name = document.getElementById("nickInput").value;
    obj.head_pic = document.getElementById("headImg").src;
    obj.gender = getRadioValue("gender");
    obj.desc = document.getElementById("infoTextarea").value;
    obj.phone_num = document.getElementById("phone").value;
    obj.wechat = document.getElementById("wechat").value;
    obj.qq = document.getElementById("qq").value;
    
    confirmInfo = validateInfo();
    confirmNickname = validateNickname(obj.name);
    confirmPhone = validatePhone(obj.phone_num);
    confirmQQ = validateQQ(obj.qq);
    confirmWechat = validateWechat(obj.wechat);
    xmlhttp.onreadystatechange=function()
          {
              if (xmlhttp.readyState==4 && xmlhttp.status==200)
               {
                  alert("保存成功！")
              }
        }

    if (confirmInfo && confirmPhone && confirmPhone && confirmQQ &&confirmWechat){
    /* 通过js对象生成一串参数形式字符，输出举例："foo=bar&lorem=ipsum" */
    var jsonObj = toParams(obj);
    console.log(jsonObj);
    xmlhttp.open("post",'/updateinfo',true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(jsonObj);
      }
    else{
      alert("保存失败！请检查输入的值")
    }
}

/* 通过js对象生成一串参数形式字符，输出举例："foo=bar&lorem=ipsum" */
function toParams(obj){
  var s = '';
  if (!obj){
    return s;
  }
  for (i in obj){
    if (!i) continue;

    s += "&" + i + "=" + obj[i];
  }

  return s;
}

/*获取radio的被选中值*/

function getRadioValue(name){
  var elems = document.getElementsByName(name)

  for (var i in elems){
    if (elems[i].checked){
      return elems[i].value;
    }
  }
}

function changeEmail(){
    verificationElem = document.getElementById('verificationEmail');
    inputElem = document.getElementById('changeEmail');

    verificationEmail.style.display = "none";
    inputElem.style = "";

     document.getElementById("leveloneNote").innerHTML = '';
}

function cancelInput(){
    verificationElem = document.getElementById('verificationEmail');
    inputElem = document.getElementById('changeEmail');

    verificationEmail.style = "";
    inputElem.style.display = "none";

}

function storeChange(){
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
    }
  else
    {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    verificationElem = document.getElementById('verificationEmail');
    inputElem = document.getElementById('changeEmail');

    var obj = new Object();
    obj.userid = document.getElementsByClassName("setting")[0].id;
    obj.newEmail = document.getElementById('inputChangeEmail').value;
    /*验证输入的邮箱是否合法，不符合会返回不符合的原因字符串，所以失败验证返回的是非空值*/
    confirm = validateEmail('inputChangeEmail');

    /* 失败返回false， 成功返回true*/
    confirmSign = checkEmail(obj.newEmail);
    console.log(confirmSign)
    /*验证失败*/
    if(confirm)
    {
      document.getElementById("leveloneNote").innerHTML = confirm;
    }
  
    else if (!confirmSign){
      document.getElementById("leveloneNote").innerHTML = "该邮箱已被注册！";
    }
    /*验证通过*/
    
    else{
          document.getElementById('emailMsg').innerHTML="邮箱为网站唯一登录账号，非常重要";
          verificationEmail.style = "";
          inputElem.style.display = "none";
          verificationEmail.style = "";
          inputElem.style.display = "none";
          document.getElementById("sendMail").style = '';
          document.getElementById("sendMail").innerHTML = '发送验证邮件';
          document.getElementById("sendMail").disabled = false;
          document.getElementById("verificationNote").innerHTML = '';
          xmlhttp.onreadystatechange=function()
          {
              if (xmlhttp.readyState==4 && xmlhttp.status==200)
               {
                document.getElementById('settingEmail').innerHTML=obj.newEmail;
                document.getElementById('inputChangeEmail').value = '';
              }
        }
        /* 通过js对象生成一串参数形式字符，输出举例："foo=bar&lorem=ipsum" */
        var params = toParams(obj);
        console.log(params);
        xmlhttp.open('get','/newemail/store?' + params,true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send();
    }

}
function sendEmail(){
    var elem = document.getElementById('sendMail')
    if (elem.innerHTML == "登录邮箱验证"){
      return false;
    }
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
    }
  else
    {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    var obj = new Object();
    obj.userid = document.getElementsByClassName("setting")[0].id;
    obj.newEmail = document.getElementById('settingEmail').innerHTML;
    var params = toParams(obj);
    console.log(params);
    xmlhttp.open('get','/newemail/send?' + params,true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send();

    xmlhttp.onreadystatechange=function()
      {
          if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
            document.getElementById('verificationNote').innerHTML=" 发送成功";
            
            var elem = document.getElementById('sendMail')
            elem.innerHTML = '登录邮箱验证';
            elem.style.backgroundColor = 'gray';
            document.getElementById('emailMsg').innerHTML="请验证邮箱。如已验证，请刷新页面";
        }
        }
}

function transferFous(toId){
    document.getElementById(toId).focus();
}

function hideLabel(id){
    document.getElementById(id).style.display = "none";
}

/*验证登录的输入框*/
function validate_login(){
    console.log("validate_login");
    var msg = validateEmail('username');
    
    var passwd = document.getElementById("passwd").value;

    console.log(msg);
    if (msg){
      document.getElementById('login_input_note').innerHTML = msg;
      $('.input_note').addClass('warning_note');
      return false;
    }
    else if (!passwd.length){
      document.getElementById('login_input_note').innerHTML = "密码不能为空！";
      $('.input_note').addClass('warning_note');
      return false;
    }

    else{
      return true;
    }
}

/ * 验证邮箱是否已被注册，以来后台接口 */
function checkEmail(email){

    var confirm;

    var res = $.ajax({url:'/email/check?email=' + email, async:false});

    //console.log(res.responseText);

    if (res.responseText == 'valid'){
      return true;
    }
    else{
      return false;
    }

}
/*验证注册的输入框*/
function validate_signup(){
  var msg = validateEmail('username');
  var passwd = document.getElementById("passwd").value;
  var passwd2 = document.getElementById("passwd2").value;
  var auth_code = document.getElementById("input_auth_code").value;
  var email = document.getElementById('username').value;
  if (msg){
      document.getElementById('login_input_note').innerHTML = msg;
      $('.input_note').addClass('warning_note');
      return false;
    }

  else if(auth_code.search("^[a-zA-Z0-9]{4,5}$") <0 ){
      console.log("请输入有效的验证码");
      $('.input_note').html("请输入有效的验证码");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else if(passwd.length<6 || passwd.length >24){
      $('.input_note').html("密码必须是6至24位字符");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else if(passwd != passwd2){
      $('.input_note').html("两次输入的密码不相等");
      $('.input_note').addClass('warning_note');
      return false;
  }

  else{
    return true;
  }

}
function search_submit(){
  var inputId = "search_text";
  var selectId = "search_type";

  obj = new Object();
  obj.type = document.getElementById(selectId).value;
  obj.text = document.getElementById(inputId).value;
  if (!obj.text){
    /*如果输入的值为空，点击搜索无反应*/
    return false;
  }
  params = toParams(obj);

  url = "/search?" + params;
  window.location.href = url;
}


function range(start, end, interval){
    var types = typeof start;
    var typee = typeof end;

    if (types != typee){
      console.log("please input two valid value");
      return false;
    }

    var result = new Array();
    var j = 0;
    if (types == "number") {
      for (i=start; i<end;i += interval){
          result[j] = i;
          j++;
      }
    }

    else if (types=="string" && start.length == 1 && end.length == 1){
      //转化为对应字符编码号
      start = start.charCodeAt(0);
      end = end.charCodeAt(0);
      
      for (i=start; i<end;i += interval){
          //从编码号转回字符
          result[j] = String.fromCharCode(i);
          j++;
      }
    }
    else{
      console.log("please input two valid value");
      return false;
    }
  
  return result
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

  //页面发生跳转后，先去除选择的那个页签类

  if (cur){
    $('.pagenum').removeClass('pageSelected');
  }
  console.log('remove pageSelected class');
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
  //document.getElementById("scrollControl").scrollTop = 0;
}

function getParamValue(key){
    url = document.URL;
    if (url.indexOf('?') == -1){
      return 1
    }
    regex = key + '=' + '([^&]*)';
    value = url.match(regex);
    return value[1]
}

function renderRecord(){
    url = document.URL;

    if (url.indexOf('collect') > -1){
          $('.btn_nav').removeClass('btn_selected');
          $('.my_collects').addClass('btn_selected');
          console.log('my_collects page');
    }
    console.log('renderRecord finished');
}

function getAuthCodeNoSignCheck(id)
{
  console.log('get auth code');
  document.getElementById('login_input_note').innerHTML = "";
  $('.input_note').removeClass('warning_note');
  msg = validateEmail('username');
  var str = document.getElementById("username").value;
  /*倒计时的时候不可点击*/
  if (document.getElementById(id).innerHTML.lastIndexOf("秒") > -1){ 
    console.log("false");
    return false;
  }
  //验证邮箱输入
  if (msg){
    document.getElementById('login_input_note').innerHTML = msg
    $('.input_note').addClass('warning_note');
    return false
  }

  xmlhttp = getXmlhttp();

  xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    count(60,id);
    
    }
  }
    xmlhttp.open("GET","/auth_code?username="+str,true);
    xmlhttp.send();
}

function validate_find(){
    var msg = validateEmail('username');
    var auth_code = document.getElementById("input_auth_code").value;
    var email = document.getElementById('username').value;
    if (msg){
        document.getElementById('login_input_note').innerHTML = msg;
        $('.input_note').addClass('warning_note');
        return false;
      }

    else if(auth_code.search("^[a-zA-Z0-9]{4,5}$") <0 ){
        console.log("请输入有效的验证码");
        $('.input_note').html("请输入有效的验证码");
        $('.input_note').addClass('warning_note');
        return false;
    }

    else{
      return true;
  }
}

function validate_reset(){

  var passwd = document.getElementById("passwd").value;
  var passwd2 = document.getElementById("passwd2").value;

  if(passwd.length<6 || passwd.length >24){
      $('.input_note').html("密码必须是6至24位字符");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else if(passwd != passwd2){
      $('.input_note').html("两次输入的密码不相等");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else{
    return true;
  }
}


function validate_change(){
  var passwd0 = document.getElementById("passwd0").value;
  var passwd = document.getElementById("passwd").value;
  var passwd2 = document.getElementById("passwd2").value;
  
  if(passwd0.length<6 || passwd0.length >24){
      $('.input_note').html("密码必须是6至24位字符");
      $('.input_note').addClass('warning_note');
      return false;
  }

  if(passwd.length<6 || passwd.length >24){
      $('.input_note').html("密码必须是6至24位字符");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else if(passwd != passwd2){
      $('.input_note').html("两次输入的密码不相等");
      $('.input_note').addClass('warning_note');
      return false;
  }
  else{
    return true;
  }
}

function deleteItems(url){
  var elems = $('.single_check:checked');
  var items = '';
  if (elems.length == 0){
    alert("请至少选择一个要删除的项目！");
    return false;
  }

  for (i=0; i<elems.length;i ++){
    items += ',' + elems[i].value;
    c_status = $('#' + 'status_' + elems[i].value).attr("value");
    if (c_status != 0){
      alert("只能删除未审核状态的项目");
      return false
    }
  }

  console.log(items);
  var r =confirm("确认删除选中的项目？");
  if (r == true){
    $.post(url,{
      items:items,
    },function(data,status){
      if (status == "success" && data=="success"){
        alert("删除成功！")
        //刷新页面
        window.location.reload(true);
      }
      else{
        alert("删除失败！");
      }
    });
  }
  else{
    return false;
  }

}

function deleteLesson(url){
  var elems = $('.single_check:checked');
  var items = '';
  cid = $('.course_manage').attr('id');
  if (elems.length == 0){
    alert("请至少选择一个要删除的项目！");
    return false;
  }

  for (i=0; i<elems.length;i ++){
    items += ',' + elems[i].value;
  }

  console.log(items);
  var r =confirm("确认删除选中的项目？");
  if (r == true){
    $.post(url,{
      items:items,
      cid:cid,
    },function(data,status){
      if (status == "success" && data=="success"){
        alert("已提交删除申请, 需要审核！");
        window.location.reload(true);
        return true
      }
      else{
        alert("删除失败！");
        return false
      }
    });
  }
  else{
    return false;
  }

}

 function submit_course(url){
      course_name = $('input[name="course_title"]').val();
      course_item_image = $('#headImg').attr('src');
      course_desc = $('.course_desc').val();
      category_id = $('.course_category').val();
      sub_id = $('.sub_category').val();
      course_id = $('.op_title').attr('id');
      if (course_name<4 || course_name.length>20){
          $('.warn_course_create').html("课程名必须在4至20字符之间");
          return false;
      }
      else if (!course_item_image){
          $('.warn_course_create').html("请上传课程预览图片！");
          return false;
      }

      else if (!course_desc){
        $('.warn_course_create').html("请添加课程描述，方便更多人学习它！");
         return false;
      }
      else{
      $.post(url,{
        course_title: course_name,
        pic:course_item_image,
        desc:course_desc,
        category_id:category_id,
        sub_id:sub_id,
        course_id:course_id,
      },
      function(data,status){
        if (data !='success'){
          $('.warn_course_create').html(data);
          return false;
        }
        else{
          $('.for_close').css('z-index','-999');
          window.location.reload(true);
        }
      });}
    }

      //点击关闭按钮
function close_low(){
      $('.for_close').css('z-index','-999');
    }

function select_change(){
      category_id = $('.course_category').val();

      $.get('/subselect/' + category_id,function(data,status){
        $('.sub_category').html(data);
});}


//新建课程，课时
function create(url){
        $('.for_close').css('z-index','999');
        $.get(url,function(data, status){
          if (status == "success"){
            $('.for_close').html(data);
          }
        });
    }
//提交课时信息
function submit_video(url){
      course_name = $('input[name="course_title"]').val();
      course_item_image = $('#headImg').attr('src');
      course_desc = $('.course_desc').val();
      course_id = $(".op_title").attr('id');
      duration = $(".v_create")[0].duration;
      vid = $('.title').attr('id');
      if (course_name<4 || course_name.length>20){
          $('.warn_course_create').html("课时名必须在4至20字符之间");
          return false;
      }
      else if (!course_item_image){
          $('.warn_course_create').html("请上课时视频！");
          return false;
      }

      else if (!course_desc){
        $('.warn_course_create').html("请添加课时描述，方便更多人学习它！");
         return false;
      }
      else{
      $.post(url,{
        video_title: course_name,
        video_url:course_item_image,
        desc:course_desc,
        course_id:course_id,
        duration:duration,
        vid:vid,
      },
      function(data,status){
        if (data !='success'){
          $('.warn_course_create').html(data);
          return false;
        }
        else{
          $('.for_close').css('z-index','-999');
          $('.c_info').val('');
          $('#headImg').removeAttr('src');
          window.location.reload(true);
        }
      });}
    }

function audit(url){
        var elems = $('.single_check:checked');
        var items = '';
        if (elems.length == 0){
              alert("请至少选择一个审核的项目！");
              return false;
        }

        for (i=0; i<elems.length;i ++){
              
              c_status = $('#' + 'status_' + elems[i].value).attr("value");
              if (c_status == 1 || c_status == 2){
                    alert("不要重复提交已审核或审核中的项目！");
                    return false
                }
              items += ',' + elems[i].value;
              }
        console.log(items);
        var r =confirm("确认提交审核选中的项目？");
        if (r == true){
        $.post(url,{
            items:items,
          },function(data,status){
            if (status == "success" && data=="success"){
              alert("提交成功！");
              window.location.reload(true);
            }
          else{
            alert("提交失败！");
            }
           });
          }
        else{
            return false;
}}

function f_audit(url){
        var elems = $('.single_check:checked');
        var items = '';
        var single = $('.course_manage').attr('id');
        if (single){
          items += single;
        }

        if (elems.length == 0 && !single){
              alert("请至少选择一个审核的项目！");
              return false;
        }

        for (i=0; i<elems.length;i ++){
              c_status = $('#' + 'status_' + elems[i].value).attr("value");
              items += ',' + elems[i].value;
              }
        console.log(items);
        var r =confirm("确认审核通过选中的项目？");
        if (r == true){
        $.post(url,{
            items:items,
          },function(data,status){
            if (status == "success" && data=="success"){
              alert("审核成功！");
              window.location.reload(true);
            }
          else{
            alert("审核失败！");
            }
           });
          }
        else{
            return false;
}}

function clearLabel(){
    var username = $('#username').val();
    var passwd = $('#passwd').val();

    console.log('username:' + username);
    console.log('passwd: ' + passwd);
    if (username){
      $('#username_note').css('display','none');
    }
    if (passwd){
      $('#passwd_note').css('display','none');
    }
}