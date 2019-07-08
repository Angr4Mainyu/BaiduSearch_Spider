layui.use(['layer', 'element', 'form'], function () {
    var layer = layui.layer,
        form = layui.form,
        element = layui.element;

    // 目录
    var siteDir = $('.site-dir');
    if (siteDir[0] && $(window).width() > 750) {
        var index = layer.open({
            type: 1,
            title: "目录",
            shade: 0,
            closeBtn: 0,
            content: $('#page-index'),
            area: '150px',
            offset: 'r',
            skin: 'layui-layer-lan',
            button: false,
            success: function (layero, index) {
                layer.style(index, {
                    marginLeft: -20
                });
            }
        })
    }

    //重新给指定层设定width、top等
    layer.style(index, 'magrin-left:-20px;');

    //窗口scroll
    ; !function () {
        var main = $('.site-tree').parent(), scroll = function () {
            var stop = $(window).scrollTop();

            if ($(window).width() <= 750) return;
            var bottom = $(document).height() - $(window).height();
            if (stop > 60 && stop < bottom) {
                if (!main.hasClass('site-fix')) {
                    main.addClass('site-fix');
                }
                if (main.hasClass('site-fix-footer')) {
                    main.removeClass('site-fix-footer');
                }
            } else if (stop >= bottom) {
                if (!main.hasClass('site-fix-footer')) {
                    main.addClass('site-fix site-fix-footer');
                }
            } else {
                if (main.hasClass('site-fix')) {
                    main.removeClass('site-fix').removeClass('site-fix-footer');
                }
            }
            stop = null;
        };
        scroll();
        $(window).on('scroll', scroll);
    }();

    //让导航在最佳位置
    var setScrollTop = function (thisItem, elemScroll) {
        if (thisItem[0]) {
            var itemTop = thisItem.offset().top
                , winHeight = $(window).height();
            if (itemTop > winHeight - 120) {
                elemScroll.animate({ 'scrollTop': itemTop / 2 }, 200)
            }
        }
    }
    setScrollTop($('.site-demo-nav').find('dd.layui-this'), $('.layui-side-scroll').eq(0));
    setScrollTop($('.site-demo-table-nav').find('li.layui-this'), $('.layui-side-scroll').eq(1));


    //手机设备的简单适配
    var treeMobile = $('.site-tree-mobile')
        , shadeMobile = $('.site-mobile-shade')

    treeMobile.on('click', function () {
        $('body').addClass('site-mobile');
    });

    shadeMobile.on('click', function () {
        $('body').removeClass('site-mobile');
    });

    window.onload = function() {
        var title = $('title').text();
        $("cite:contains(" + title + ")").parent().parent().addClass('layui-this')
    }
})