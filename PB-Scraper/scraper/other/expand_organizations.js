(async function() {
    async function expand_ul(anchor, path) {
        var items = anchor.querySelectorAll(path + " > li");
        for (var i = 0; i < items.length; i++) {
            var pwd = path + " > li:nth-child(" + (i + 1) + ")";
            var button = anchor.querySelector(pwd + " button[aria-expanded='false']");
            if (button === null) continue;
            button.click();
            await new Promise(resolve => setTimeout(resolve, 300));
            pwd += " > ul";
            var lower_level = anchor.querySelector(pwd);
            if (lower_level === null) continue;
            await expand_ul(anchor, pwd);
        }
    }
    var path = "li#ttree\\:0 > ul";
    await expand_ul(document, path);
})();
