// pages/object/object.js
var id = null
var un = 0

Page({

  /**
   * 页面的初始数据
   */
  data: {
    un: 0,
    oid: 0,
    noId: false,
    warn: false,
    warntext: '',
    father: '',
    where: '',
    usable: '',
    remark: '',
    loading: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    id = getApp().globalData.objectId
    this.setData({
      loading: true
    })
    console.log("开始加载")
    var that = this
    if (id == null) {
      this.setData({
        noId: true,
        loading: false
      })
    } else {
      this.setData({
        oid: id
      })
      getApp().globalData.objectId = null
      wx.request({
        url: getApp().globalData.apiUrl + 'object',
        data: {
          id: String(id),
          key: getApp().globalData.key,
          openid: getApp().globalData.openid
        },
        success: function(res) {
          if (res.statusCode != 200) {
            that.setData({
              warn: true,
              warntext: "异常错误\n错误代码：" + res.statusCode
            })
          } else {
            un = res.data.un
            that.setData({
              un: res.data.un,
              where: res.data.where,
              father: res.data.father,
              usable: res.data.usable,
              remark: res.data.remark
            })
            console.log("加载完成")
          }
        },
        complete: function () {
          that.setData({
            loading: false
          })
        }
      })
    }
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
    if (id == null) {
      this.setData({
        noId: true
      })
    }
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


  closeit: function () {
    this.setData({
      noId: false
    })
    wx.switchTab({
      url: '/pages/list/list',
    })
  },


  close: function () {
    this.setData({
      warn: false
    })
    wx.navigateBack({
      delta: 0,
    })
  },
  

  cl: function () {
    if (id != null) {
      wx.navigateTo({
        url: '/pages/operation/operation?id=' + id + "&usable=" + un,
      })
    }
  }
})