$(document).ready(function(){
        //图标默认路径
        $.fn.raty.defaults.path = '/static/ratylib/img';
        
        $('.rate_add').raty({
                 hints: ['极差','差', '一般', '好', '非常好'],
                 half:true,
                 space:false,
                 //click: function(score) {
                 //console.log("score: " + score);
                    //$(this).raty({ 
                        //readOnly: true,
                        //score:score,
                    //});
                    //}
             });

        //获取每个用户对本课程的评分，并渲染星星图

        $('.rate_display').raty(
            {
                half:true,
                score:function(){
                    return $(this).attr('score');
                },
                space:false,
                readOnly:true,
            });

        $(".course_nav_item").on("click", function(){
            if ($(this).attr("class").indexOf("course_selected") > -1){
                return false;
            }

            $(".course_nav_item").removeClass("course_selected");
            $(this).addClass("course_selected");

            //显示目录
            if ($(this).attr("class").indexOf("li_catalog") > -1){
                console.log("li_catalog");
                $(".catalog").css("display","");
                $(".course_detail").css("display","none");

            }
            //显示详情
            if ($(this).attr("class").indexOf("li_details") > -1){
                console.log("li_details");
                $(".course_detail").css("display","");
                $(".catalog").css("display","none");
            }
        });

        $('.comment_submit').click(function(){
            course_id = $('.course_info').attr('course_id');
            score = $('.rate_add_course input[name="score"]').attr('value');
            comment = $('.inputCheck').val();


            if (!score || !course_id){
                console.log('course id: ' + course_id);
                console.log('score: '+ score);
                return false;
            }

            url = '/course/score?course_id=' + course_id + '&' + 'score=' + score + '&' + 'comment=' + comment
            console.log(url);
            $.get(url, function(data,status){
                    console.log(status);
                    console.log(data);
                    $('#commentUl').prepend(data);
                    $('.rate_title').html('您已给课程打分');
                    $('.rate_display').raty({
                        half:true,
                        score:function(){
                            return $(this).attr('score');},
                        space:false,
                        readOnly:true,
                        });
                    $('.rate_remove').remove();
                    $('.user_rate_area').css('height','50px')
                    $('.rate_add').raty({
                            half:true,
                            score:score,
                            space:false,
                            readOnly:true,
                            });
                });
        });
    //差异化学习进度的背景色
    $("span:contains(%)").addClass('inprogress');
    $("span:contains(完成)").addClass('inprogress');



});//end of document


