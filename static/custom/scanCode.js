function upload() {
    document.querySelector('#filein').click();
}

function decode(src){

    var reader = new FileReader();
    reader.onload = function(){
        var fd = new FormData;
        console.log(src);
        var fff = this.result;
        console.log(fff)
        fd.append('u', 'file');
        fd.append('filein', fff);
        s=$.ajax({
                type: "post",
                url:  "https://rm.bismarck.xyz/scan",
                data: fd,
                processData: false, //告诉jquery要传输data对象
                contentType: false,   //告诉jquery不需要增加请求头对于contentType的设置
                async: true,    //默认是true：异步，false：同步。
                success: function (data) {
                    window.location.href="https://rm.bismarck.xyz/object?id=" + data;
                },
                error: function (data) {
                    alert("未知错误");
                },

    });
    }
    reader.readAsDataURL(src);
}