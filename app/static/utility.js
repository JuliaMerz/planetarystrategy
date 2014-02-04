function loadArticle(id) {
    "use strict";
    $('#article-' + id).load('/get-article/' + id);
}
  
function loadArticlePreview(id) {
    "use strict";
    $('#article-' + id).load('/get-article-preview/' + id);
}