// pages/operation/operation.js
var newClass = [false, true, false, false]
var newObj = [true, false, true, false]
var proUse = [false, false, false, true]
var inHome = [true, false, false, false]
var allNo = [false, false, false, false]

var nc = ["新增物资"]
var no = ["新增对象"]
var usable = ["项目使用", "借出", "送修", "报废"]
var using = ["还入", "送修", "报废"]
var repairing = ["结束送修"]
var can = ["取消报废"]
var leave = ['请假一天', '请假两天', '请假三天']

var opk = [["新增物资"], ["新增对象"], ["项目使用", "借出", "送修", "报废"], ["还入", "送修", "报废"], ["结束送修"], ["取消报废"], ['请假一天', '请假两天', '请假三天']]

var kind = 0
var usable = 0
var opid = 0

Page({

  /**
   * 页面的初始数据
   */
  data: {
    id: 0,
    open: [false, false, false, false],
    opKind: [],
    index: 0,
    loading: false,
    idopen: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      id: options.id,
    })
    if (options.id != null) {
      if (options.id == 0) {
        console.log('leave')
        kind = 6
        this.setData({
          idopen: false
        })
      } else if (options.id < 1000000) {
        kind = 1
      } else {
        usable = Number(options.usable)
        switch (usable) {
          case 0: kind = 3; break;
          case 1: kind = 2; break;
          case 2: kind = 4; break;
          case 3: kind = 5; break;
        }
      }
    } else {
      kind = 0
    }
    if (kind == 0) {
      this.setData({
        idopen: false
      })
    }
    this.setData({
      opKind: opk[kind]
    })
    refersh(this)
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

  close: function () {
    this.setData({
        iosDialog2: false,
        loading:false
    })
  },

  pchange: function(e) {
    this.setData({
      index: Number(e.detail.value)
    })
    refersh(this)
  },

  formSubmit: function(e) {
    var that = this
    this.setData({
      loading: true
    })
    var ok = true
    for (var a in Object.values(e.detail.value)) {
      if (!check(Object.values(e.detail.value)[a], that)) {
        ok = false
      }
    }
    if (ok) {
      var send = e.detail.value
      send.openid = getApp().globalData.openid
      switch (kind) {
        case 0: send.op = "addc"; break;
        case 1: send.op = "addo"; break;
        case 2: {
          switch (this.data.index) {
            case 0: send.op = "use"; break;
            case 1: send.op = "out"; break;
            case 2: send.op = "re"; break;
            case 3: send.op = "bf"; break;
          }
          break;
        }
        case 3: {
          switch (this.data.index) {
            case 0: send.op = "in"; break;
            case 1: send.op = "re"; break;
            case 2: send.op = "bf"; break;
          }
          break;
        }
        case 3: send.op = "cre"; break;
        case 4: send.op = "cbf"; break;
        case 6: {
          send.op = 'leave'
          var days = Number(this.data.index) + 1
          send.oid = String(days) + '天'
          send.num = String(days)
        }
        break;
      }
      send.key = getApp().globalData.key
      console.log(send)
      wx.request({
        url: getApp().globalData.apiUrl + 'operation',
        data: send,
        success: function(res) {
          if (res.statusCode != 200) {
            if (res.statusCode == 401) {
              that.setData({
                tips: "您的账号尚未认证，请在“我”中提交注册申请并等待通过后再试",
                iosDialog2: true
              })
            } else {
              that.setData({
                tips: "请求时发生错误\n错误代码: " + res.statusCode,
                iosDialog2: true
              })
            }
          } else {
            console.log(res.data)
            if (res.data != "wait") {
              that.setData({
                tips: "操作成功",
                iosDialog2: true
              })
            } else {
              that.setData({
                tips: "提交成功\n管理员审核通过后生效",
                iosDialog2: true
              })
            }
          }
        },
        fail: function(res) {
          that.setData({
            tips: "异常错误",
            iosDialog2: true
          })
        }
      })
    }
  }
})

function refersh(p) {
  var opp = null
  switch (kind) {
    case 0: opp = newClass; break;
    case 1: opp = newObj; break;
    case 2: {
      switch (p.data.index) {
        case 0: opp = proUse; break;
        default: opp = allNo; break;
      }
      break;
    }
    case 3: {
      switch (p.data.index) {
        case 0: opp = inHome; break;
        default: opp = allNo; break;
      }
      break;
    }
    case 6: opp = allNo; break;
    default: opp = inHome; break;
  }
  p.setData({
    open: opp
  })
}

function check(v, p){
  if((v).length!=0){
    var reg=/^[\u4e00-\u9fa5_a-zA-Z0-9-]{1,200}$/g;
    if(!reg.test(v)){
      p.setData({
        tips: "对不起，输入的内容仅支持中英文、数字、减号或下划线",
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