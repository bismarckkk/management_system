// pages/register/register.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    toast: false,
    loading: false,
    hideToast: false,
    hideLoading: false,
    tips: "",
    iosDialog2: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  
  formSubmit: function(e) {
    console.log(e.detail.value)
    var r1 = check(e.detail.value.st_n, this)
    console.log(r1)
    var r2 = check(e.detail.value.re_n, this)
    var that = this
    if (r1 && r2) {
      openLoading(this)
      wx.request({
        url: getApp().globalData.apiUrl + 'register/submit',
        data: {
          key: getApp().globalData.key,
          st: e.detail.value.st_n,
          re: e.detail.value.re_n,
          openid: getApp().globalData.openid
        },
        success: function(res) {
          if (res.statusCode != 200) {
            console.error('获取失败')
          } else {
            console.log(res.data)
            openToast(that)
          }
        },
        fail: function() {
          that.setData({
            tips: "异常错误",
            iosDialog2: true
          })
        }
      })
    }
  },

  close: function () {
    this.setData({
        iosDialog2: false,
    })
  },
})

function check(v, p){
  if((v).length!=0){
    var reg=/^[\u4e00-\u9fa5_a-zA-Z0-9-]{1,16}$/g;
    if(!reg.test(v)){
      p.setData({
        tips: "对不起，输入的内容限16个字符，支持中英文、数字、减号或下划线",
        iosDialog2: true
      })
      return false
    } else {
      return true
    }
  } else {
    p.setData({
      tips: "请填写信息",
      iosDialog2: true
    })
    return false
  }
}

function openToast(p) {
    p.setData({
        loading: false,
        toast: true
    });
    setTimeout(() => {
        p.setData({
            hideToast: true
        });
        setTimeout(() => {
            p.setData({
                toast: false,
                hideToast: false,
            });
        }, 300);
    }, 3000);
}

function openLoading(p) {
  p.setData({
      loading: true
  });
  setTimeout(() => {
      p.setData({
          hideLoading: true
      });
      setTimeout(() => {
          p.setData({
              loading: false,
              hideLoading: false,
          });
      }, 300);
  }, 3000);
}