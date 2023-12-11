document.addEventListener('DOMContentLoaded', function() {
    let footer = document.querySelector('footer');
    var html = document.documentElement;
    var body = document.body;
    function isAtBottom() {
        let scrollTop = window.scrollY || document.documentElement.scrollTop;
        let windowHeight = window.innerHeight || document.documentElement.clientHeight;
        let bodyHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
    return scrollTop + windowHeight >= bodyHeight;
    }

    function handleScroll() {
        if (isAtBottom()){
            footer.classList.remove('d-none');
            increasePageHeight()
            console.log("Hehe")
        } else {
            footer.classList.add('d-none');
        }
    }
    function increasePageHeight() {
        html.style.height = '135%';
        body.style.height = '135%';
        console.log(html.style.height)
    }
    window.addEventListener('scroll', handleScroll)
}
);