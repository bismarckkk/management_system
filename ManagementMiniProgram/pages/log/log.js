// pages/log/log.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    oid: null,
    time: null,
    object: null,
    name: null,
    operation: null,
    verify: null,
    wis: null,
    do: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var item = getApp().globalData.logList[options.id]
    this.setData({
      oid: item.id,
      time: item.time,
      object: item.object,
      name: item.name,
      operation: item.operation,
      verify: item.verify,
      wis: item.wis,
      do: item.do
    })
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

  }
})