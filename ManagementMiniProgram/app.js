//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    var that = this
    this.globalData.mready = false
    wx.getBackgroundFetchData({
      fetchType: 'pre',
      success(res) {
        var d = JSON.parse(res.fetchedData)
        getApp().globalData.openid = d.openid
        getApp().globalData.key = d.key
        getApp().globalData.u = d.u
        console.log(d.u)
        getApp().globalData.mready = true
        var i = 0
        var a = setInterval(function () { 
          i++
          if(i >= 60 || that.globalData.listPage != null)
          { 
              function f2 () {
                getApp().globalData.listPage.setData({
                  mlist: JSON.parse(d.mlist),
                  adapterSource: d.words,
                  loading: false
                })
                if (d.u == 2) {
                  that.globalData.listPage.setData({
                    admin: true
                  })
                }
              }
              f2()
              clearInterval(a) 
          } 
        }, 50)
      }
    })
    
    // 登录
    wx.login({
      success: res => {
        if (res.code){
          wx.request({
            url: getApp().globalData.apiUrl + 'getUserInfo',
            data: {
              code: res.code,
              key: getApp().globalData.key
            },
            success (res) {
              if (res.statusCode != 200) {
                console.error('获取失败')
              } else {
                console.log(res.data.openid)
                getApp().globalData.openid = res.data.openid
                getApp().globalData.key = res.data.key
                getApp().globalData.u = res.data.u
                wx.setBackgroundFetchToken({
                  token: res.data.openid
                })
              }
            }
          })
        } else {
          console.error('登录失败')
        }
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    apiUrl: "https://rm.bismarck.xyz/wx/",
    // 注意上面的url必须以/结尾
    userInfo: null,
    openid: null,
    objectId: null,
    key: null,
    u: 0,
    mlist: null,
    words: null,
    listPage: null,
    mready: false,
    logList: null
  }
})