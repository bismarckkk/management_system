// pages/listObj/listObj.js
var id = 0
var k
var t
var f

Page({

  /**
   * 页面的初始数据
   */
  data: {
    obj: null,
    mlist: [],
    e: false,
    loading: false,
    admin: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    this.setData({
      loading: true
    })
    if (getApp().globalData.u == 2) {
      this.setData({
        admin: true
      })
    }
    if (options.k == "o") {
      wx.request({
        url: getApp().globalData.apiUrl + 'getList',
        data: {
          k: "o",
          f: options.f,
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            that.setData({
              mlist: res.data,
              obj: Object.keys(res.data)[0]
            })
            id = parseInt(Object.values(res.data)[0][0].id / 100)
          } else {
            that.setData({
              e: true
            })
          }
        },
        fail: function () {
          that.setData({
            e: true
          })
        },
        complete: function() {
          that.setData({
            loading: false
          })
        }
      })
    } else {
      wx.request({
        url: getApp().globalData.apiUrl + 'getList',
        data: {
          k: "s",
          t: options.t,
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            that.setData({
              mlist: res.data
            })
          } else {
            that.setData({
              e: true
            })
          }
        },
        fail: function () {
          that.setData({
            e: true
          })
        },
        complete: function() {
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

  /*
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    if (getApp().globalData.u == 2) {
      this.setData({
        admin: true
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

  add: function() {
    wx.navigateTo({
      url: '/pages/operation/operation?id=' + id,
    })
  },

  goto: function(e) {
    getApp().globalData.objectId = e.currentTarget.dataset.id
      wx.reLaunch({
        url: '/pages/object/object',
      })
  },

  close: function () {
    this.setData({
      e: false
    })
  },

  retry: function () {
    this.setData({
      e: false,
      loading: true
    })
    var that = this
    if (k == "o") {
      wx.request({
        url: getApp().globalData.apiUrl + 'getList',
        data: {
          k: "o",
          f: f,
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            that.setData({
              mlist: res.data,
              obj: Object.keys(res.data)[0]
            })
            id = parseInt(Object.values(res.data)[0][0].id / 100)
          } else {
            that.setData({
              e: true
            })
          }
        },
        fail: function () {
          that.setData({
            e: true
          })
        },
        complete: function() {
          that.setData({
            loading: false
          })
        }
      })
    } else {
      wx.request({
        url: getApp().globalData.apiUrl + 'getList',
        data: {
          k: "s",
          t: t,
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            that.setData({
              mlist: res.data
            })
          } else {
            that.setData({
              e: true
            })
          }
        },
        fail: function () {
          that.setData({
            e: true
          })
        },
        complete: function() {
          that.setData({
            loading: false
          })
        }
      })
    }
  }
})