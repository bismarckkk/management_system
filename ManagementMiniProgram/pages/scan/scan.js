// pages/scan/scan.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    e: false,
    text: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    scan(this)
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

  clink: function() {
    scan(this)
  },

  close: function() {
    this.setData({
      e: false
    })
  },

  retry: function() {
    this.setData({
      e: false
    })
    scan(this)
  }
})

function scan(p) {
  wx.scanCode({
    onlyFromCamera: false,
    scanType: ['datamatrix', 'barCode'],
    success: function(res) {
      console.log(res.result)
      getApp().globalData.objectId = res.result
      wx.reLaunch({
        url: '/pages/object/object',
      })
    },
    fail: function(res) {
      getApp().globalData.objectId = null
      console.error(res)
      p.setData({
        e: true,
        text: res.errMsg
      })
    }
  })
}