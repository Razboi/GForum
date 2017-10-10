$(document).ready(function(){

  function showReplyForm()
  {
    $(this).parent().next(".reply_form").toggle();
  };

// ---------------------------------------------------

  function cancelReply()
  {
    $(this).parent().toggle();
  };

  $(".reply_link").click(showReplyForm);
  $(".reply_pm").click(showReplyForm);
  $(".cancel_reply").click(cancelReply);

// ---------------------------------------------------

  function showReplies()
  {
    $(this).next(".show_replies").toggle();
    $(this).find("i").toggleClass("fa-caret-down fa-caret-up");
  };

  $(".replies_link").click(showReplies);

// ---------------------------------------------------

  $(".comment_toggler").click(function()
  {
    $("#comment_form").toggle();
  });

// ---------------------------------------------------

  $(".parent_content_body").text(function(index, currentText) {
    if (currentText.length > 350) {
      return currentText.substr(0,350) + " ...";
    }
  });

// ---------------------------------------------------

  $("html").click(function() {
    $(".notifications_popup").hide();
  });


  $("#notifications_icon").click(function(event)
  {
    event.stopPropagation();
    $(".notifications_popup").toggle();
  });

  $("#notifications_container").click(function(event)
  {
    event.stopPropagation();
  });

});
