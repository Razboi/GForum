$(document).ready(function(){
  $(".reply_form").hide();

  function showReplyForm()
  {
    $(this).parent().next(".reply_form").toggle();
  };

  function cancelReply()
  {
    $(this).parent().toggle();
  };

  $(".reply_link").click(showReplyForm);
  $(".cancel_reply").click(cancelReply);

  function showReplies()
  {
    $(this).next(".show_replies").toggle();
    $(this).find("i").toggleClass("fa-caret-down fa-caret-up");
  };

  $(".comment_replies_link").click(showReplies);
});
