//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: '点击头像查看日志',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    if (app.globalData.u != '0') {
      this.setData({
        ok: true,
        re: false
      })
    } else {
      this.setData({
        ok: false,
        re: true
      })
    }
  },
  clink: function() {
    wx.navigateTo({
      url: '/pages/register/register',
    })
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  onShow: function () {
    if (app.globalData.u != '0') {
      this.setData({
        ok: true,
        re: false
      })
    } else {
      this.setData({
        ok: false,
        re: true
      })
    }
  },
  punch: function () {
    wx.authorize({
      scope: 'scope.userLocation',
      success: (res) => {
        console.log('成功：' , res)
      },
      fail: (res) => {
        console.log('失败：', res)
      },
    })
    var that = this
    console.log("getsetting")
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.userLocation']) {
          wx.authorize({
            scope: 'scope.userLocation',
            success () {
              p (that)
            },
            fail () {
              that.setData({
                e: true,
                info: "授权错误\n无法获取定位权限，请检查小程序设置",
                loading: false
              })
            }
          })
        } else {
          p (that)
        }
      },
      fail () {
        that.setData({
          e: true,
          info: "授权错误\n无法获取授权信息",
          loading: false
        })
      }
    })
    var that = this
    that.setData({
      loading: true
    })
    
  },
  punchQuit: function () {
    wx.authorize({
      scope: 'scope.userLocation',
      success: (res) => {
        console.log('成功：' , res)
      },
      fail: (res) => {
        console.log('失败：', res)
      },
    })
    var that = this
    console.log("getsetting")
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.userLocation']) {
          wx.authorize({
            scope: 'scope.userLocation',
            success () {
              p (that, true)
            },
            fail () {
              that.setData({
                e: true,
                info: "授权错误\n无法获取定位权限，请检查小程序设置",
                loading: false
              })
            }
          })
        } else {
          p (that, true)
        }
      },
      fail () {
        that.setData({
          e: true,
          info: "授权错误\n无法获取授权信息",
          loading: false
        })
      }
    })
    var that = this
    that.setData({
      loading: true
    })
    
  },
  leave: function () {
    wx.navigateTo({
      url: '/pages/operation/operation?id=0',
    })
  },
  close: function () {
    this.setData({
      e: false,
      iosDialog2: false
    })
  },
  log: function () {
    wx.navigateTo({
      url: '/pages/logsInfo/info',
    })
  }
})

function p (that, quit=false) {
  if (quit) {
    var te = '签退'
    var ref = getApp().globalData.apiUrl + 'punchQuit'
  } else {
    var te = '签到'
    var ref = getApp().globalData.apiUrl + 'punchNew'
  }
  wx.startWifi({
    success: (res) => {
      console.log("start")
      wx.getWifiList({
        fail: (res) => {
          console.log(res)
          that.setData({
            e: true,
            info: "获取WIFI列表错误\n" + res.errMsg
          })
          that.setData({
            loading: false
          })
        }
      })
    },
    fail: function(res) {
      console.log(res)
      that.setData({
        e: true,
        info: "开启WIFI错误\n" + res.errMsg,
        loading: false
      })
    }
  })
  wx.onGetWifiList((res) => {
    var wifiList = new Array()
    for (var i = 0; i < res.wifiList.length; i++) {
      wifiList.push(res.wifiList[i].BSSID)
    }
    console.log(wifiList)
    wx.request({
      url: ref,
      header: {
        'content-type': 'application/json'
      },
      method: 'POST',
      data: {
        key: getApp().globalData.key,
        openid: getApp().globalData.openid,
        wifi: wifiList
      },
      success: function(res) {
        if (res.statusCode == 200) {
          if (res.data.status == 'true') {
            console.log(res.data)
            that.setData({
              iosDialog2: true,
              tips: te + "成功\n" + te + "地点：" + res.data.location,
              loading: false
            })
          } else if (res.data.status == 'retry') {
            that.setData({
              iosDialog2: true,
              tips: "重复" + te + "\n你今天已经" + te + "过了",
              loading: false
            })
          } else if (res.data.status == 'noPunch') {
            that.setData({
              iosDialog2: true,
              tips: "你还没有签到\n请先签到再签退",
              loading: false
            })
          } else {
            that.setData({
              e: true,
              info: te + "失败\n无法找到目标WIFI，请确认位于指定位置，若有其他疑问请咨询管理员",
              loading: false
            })
          }
        } else {
          that.setData({
            e: true,
            info: te + "失败\n服务器通信错误，错误代码：" + res.statusCode,
            loading: false
          })
        }
      },
      fail: function(res) {
        that.setData({
          e: true,
          info: te + "失败\n其他异常错误，错误信息：" + res.errMsg,
          loading: false
        })
      }
    })
  })
}
