
window.onload = function () {
    itqiniu.setUp({
        'domain': 'http://pom7qnm9g.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/uptoken/',
        'success': function (up, file, info) {
            var image_url = file.name;
            var image_input = document.getElementById('image-input');
            image_input.value = image_url;

            var img = document.getElementById('image-show');
            img.setAttribute('src', image_url);
        }
    });
};
