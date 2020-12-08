// pages/logsInfo/info.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    mlist: null,
    loading: true,
    e: false
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
    var that = this
    that.setData({
      loading: true
    })
    wx.request({
      url: getApp().globalData.apiUrl + 'logs',
      data: {
        key: getApp().globalData.key,
        openid: getApp().globalData.openid
      },
      success: function (res) {
        if (res.statusCode == 200) {
          console.log(res.data)
          getApp().globalData.logList = res.data
          that.setData({
            loading: false,
            mlist: res.data
          })
        } else {
          that.setData({
            e: true,
            loading: false
          })
        }
      },
      fail: function (res) {
        that.setData({
          e: true,
          loading: false
        })
      }
    })
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
  close: function () {
    this.setData({
      e: false
    })
  },
  retry: function () {
    var that = this
    that.setData({
      loading: true,
      e: false
    })
    wx.request({
      url: getApp().globalData.apiUrl + 'logs',
      data: {
        key: getApp().globalData.key,
        openid: getApp().globalData.openid
      },
      success: function (res) {
        if (res.statusCode == 200) {
          console.log(res.data)
          getApp().globalData.logList = res.data
          that.setData({
            loading: false,
            mlist: res.data
          })
        } else {
          that.setData({
            e: true,
            loading: false
          })
        }
      },
      fail: function (res) {
        that.setData({
          e: true,
          loading: false
        })
      }
    })
  }
})