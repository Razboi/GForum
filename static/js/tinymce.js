tinymce.init({
  selector: '.richtext',
  editor_selector : "richtext",
  height: "200",
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
