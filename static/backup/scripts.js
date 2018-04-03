/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2018-02-14 20:56:02
 * @version $Id$
 */
//验证邮箱是否合法
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


function getAuthCode()
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    count(60,"btn_auth_code");
    }
  }
var str = document.getElementById("username").value
xmlhttp.open("GET","/auth_code?username="+str,true);
xmlhttp.send();
}

function count(time,id){
    if (time == 0){
        document.getElementById(id).innerHTML="获取验证码"
        return true
    }
    document.getElementById(id).innerHTML = time + '秒';
    time = time - 1;
    // 拼一个javascript字符串，类似：count(time,id)
    script = "count(" + time + "," + "'" + id + "'" + ")"
    //递归
    t = setTimeout(script,1000);
}

function uploadFile(id){
  var elem = document.getElementById(id)
  elem.click()
  elem.onchange=function(){
    console.log("2inputting!!");
    _upload(id);
  }
}

function _upload(id){

  var form = document.getElementById('upload');
  formData = new FormData(form); 
  if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
    }
  else
    {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

  formData.append("uplaod",1);
  formData.append(id, document.getElementById(id).files[0]);
  
  xmlhttp.onreadystatechange=function()
    {
     if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
         console.log("xmlhttp.responseText");
        console.log(xmlhttp.responseText);
        imgElem = document.getElementById("headImg")
        imgElem.src = xmlhttp.responseText
      }
    }
  xmlhttp.open("post","/upload/images",true);
  xmlhttp.send(formData);
  }

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

    /*验证输入的邮箱是否合法*/
    confirm = validateEmail('inputChangeEmail');

    var obj = new Object();
    obj.userid = document.getElementsByClassName("setting")[0].id;
    obj.newEmail = document.getElementById('inputChangeEmail').value;
    /*验证通过*/
    if (!confirm){
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
    /*验证失败*/
    else{
      document.getElementById("leveloneNote").innerHTML = confirm;
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
  document.getElementById(id).style.display = "none"
}