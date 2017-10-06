tinymce.init({
  selector: '.richtext',
  setup: function (richtext) {
    richtext.on('submit', function (e) {
        richtext.save();
    });
  },
  height: "500",
  width: "1000",
  content_style: "p {word-wrap: break-word; overflow-x: hidden;}",
  media_dimensions: false,
  image_dimensions: false,
  menubar: false,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor textcolor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code help emoticons'
  ],
  toolbar: ' undo redo | media image link | bold italic | code emoticons',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});

tinymce.init({
  selector: '.comment_richtext',
  height: "200",
  width: "450",
  max_height: "300",
  image_dimensions: false,
  media_dimensions: false,
  content_style: "p {word-wrap: break-word; overflow-x: hidden;}",
  menubar: false,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor textcolor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code help emoticons'
  ],
  toolbar: ' undo redo | media image link | bold italic | code emoticons',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});
