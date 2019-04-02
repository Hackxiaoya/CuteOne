;(function ($) {
    music = function (options) {
        var defaults = {
            container: options.container,
            fixed: options.fixed,
            autoplay: options.autoplay,
            theme: options.theme,
            loop: options.loop,
            order: options.order,
            preload: options.preload,
            volume: options.volume,
            mutex: options.mutex,
            listFolded: options.listFolded,
            listMaxHeight: options.listMaxHeight,
        };
        if(JSON.parse(localStorage.getItem('musicList'))){
            defaults['audio'] = JSON.parse(localStorage.getItem('musicList'))
        }
        var ap = new APlayer(defaults);
        delMusic = function (index) {
            var musicList = JSON.parse(localStorage.getItem('musicList'));
            index+=1
            var name = $(".aplayer-list li:nth-child("+index+")").find("span:nth-child(3)").html();
            for( var i=0 ; i<musicList.length ; i++ ){
                if(musicList[i]["name"] == name){
                    musicList.pop(i)
                }
            }
            ap.list.remove(index-1);
            localStorage.setItem('musicList', JSON.stringify(musicList));
            event.stopPropagation();    //  阻止事件冒泡
        };
        $(".aplayer-list li").each(function (obj) {
            index = $(this).find("span:nth-child(2)").html();
            index-=1;
            $(this).find("span:last-child").before("<span class='delMusic' style='color:#666;float:right;cursor:pointer;padding:0 10px;' onclick='delMusic("+index+")'>x</span>")
        });
        return {
            ap: ap,
            addMusic:function (data) {
                var musicList = JSON.parse(localStorage.getItem('musicList'));
                if(musicList){
                    if (musicList.some(({name})=>name==data[0]["name"])){
                        for( var i=0 ; i<musicList.length ; i++ ){
                            if(musicList[i]["name"] == data[0]["name"]){
                                musicList[i]["url"] = data[0]["url"];
                            }
                        }
                        $(".aplayer-list li").each(function (obj) {
                            var name = $(this).find("span:nth-child(3)").html();
                            if(name == data[0]["name"]){
                                var index = $(this).find("span:nth-child(2)").html();
                                index-=1;
                                ap.list.switch(index);
                            }
                        });
                    }else{
                        musicList.push(data[0]);
                        ap.list.add(data);
                        $(".aplayer-list li").each(function (obj) {
                            var name = $(this).find("span:nth-child(3)").html();
                            if(name == data[0]["name"]){
                                var index = $(this).find("span:nth-child(2)").html();
                                index-=1;
                                ap.list.switch(index);
                            }
                        });
                    }
                }else{
                    musicList = [];
                    musicList.push(data[0]);
                    ap.list.add(data);
                    ap.list.switch(1);
                }

                $(".aplayer-list li").each(function (obj) {
                    var index = $(this).find("span:nth-child(2)").html();
                    index-=1;
                    if(!$(this).find("span:nth-child(4)").hasClass("delMusic")){
                        $(this).find("span:last-child").before("<span class='delMusic' style='color:#666;float:right;cursor:pointer;padding:0 10px;' onclick='delMusic("+index+")'>x</span>")
                    }else{
                        $(this).find("span:nth-child(4)").attr("onclick", "delMusic("+index+")");
                    }
                });
                localStorage.setItem('musicList', JSON.stringify(musicList));
            },
            delMusic:function () {
                ap.list.remove(index);
                event.stopPropagation();    //  阻止事件冒泡
            }
        }
    };
})(jQuery);
/*

    $(function () {
       music = new music({
            container: document.getElementById('aplayer'),
            fixed: true,
            autoplay: true,
            theme: '#FADFA3',
            loop: 'all',
            order: 'list',
            preload: 'metadata',
            volume: 0.7,
            mutex: true,
            listFolded: false,
            listMaxHeight: 90,
       });
       $("#addList").on("click",function () {
            music.addMusic([{
                name: 'name',
                artist: '未知',
                url: '1.mp3,
                theme: '#ebd0c2'
            }]);
       });
    })

 */
