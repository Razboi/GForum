$(document).ready(function(){

  function showReplyForm()
  {
    $(this).parent().next(".reply_form").toggle();
  };

  function cancelReply()
  {
    $(this).parent().toggle();
  };

  $(".reply_link").click(showReplyForm);
  $(".reply_pm").click(showReplyForm);
  $(".cancel_reply").click(cancelReply);

  function showReplies()
  {
    $(this).next(".show_replies").toggle();
    $(this).find("i").toggleClass("fa-caret-down fa-caret-up");
  };

  $(".replies_link").click(showReplies);

  function activeFilter()
  {
    var path = window.location.href;
    $(".filter").toggleClass.("active");
  };



});
$(function() {
    $("#top").on("click", function () {
    $(this).addClass('active');
    $(this).siblings().removeClass('active');
    });
  })
