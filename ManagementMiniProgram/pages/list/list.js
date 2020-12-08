var wayIndex = -1;
var school_area = '';
var grade = '';
// 当联想词数量较多，使列表高度超过340rpx，那设置style的height属性为340rpx，小于340rpx的不设置height，由联想词列表自身填充
// 结合上面wxml的<scroll-view>
var arrayHeight = 0;

Page({
  data: {
    inputShowed: false,
    inputValue: '', //点击结果项之后替换到文本框的值
    adapterSource: [], //本地匹配源
    bindSource: [], //绑定到页面的数据，根据用户输入动态变化
    showScroll: true,
    mlist: [],
    e: false,
    loading: true,
    admin: false
  },
  
  //当键盘输入时，触发input事件
  bindinput: function (e) {
    //用户实时输入值
    var prefix = e.detail.value
    //匹配的结果
    var newSource = []
    this.setData({
      inputValue: e.detail.value
    });
    if (prefix != "") { 
      // 对于数组array进行遍历，功能函数中的参数 `e`就是遍历时的数组元素值。
      this.data.adapterSource.forEach(function (e) { 
        // 用户输入的字符串如果在数组中某个元素中出现，将该元素存到newSource中
        if (e.indexOf(prefix) != -1) {
          console.log(e);
          newSource.push(e)
        }
      })
    };
    // 如果匹配结果存在，那么将其返回，相反则返回空数组
    if (newSource.length != 0) {
      this.setData({
        // 匹配结果存在，显示自动联想词下拉列表
        showScroll: true,
        bindSource: newSource,
        arrayHeight: newSource.length * 71
      })
    } else {
      this.setData({
        // 匹配无结果，不现实下拉列表
        showScroll: false,
        bindSource: []
      })
    }
  },

  // 用户点击选择某个联想字符串时，获取该联想词，并清空提醒联想词数组
  itemtap: function (e) {
    console.log(e.currentTarget.dataset.t)
    this.setData({
      // .id在wxml中被赋值为{{item}}，即当前遍历的元素值
      inputValue: e.currentTarget.dataset.t,
      // 当用户选择某个联想词，隐藏下拉列表
      showScroll: false,
      bindSource: []
    })
  },
  showInput: function () {
    this.setData({
        inputShowed: true
    });
  },
  hideInput: function () {
      this.setData({
        inputValue: "",
        inputShowed: false,
        showScroll: false
      });
  },
  clearInput: function () {
      this.setData({
        inputValue: ""
      });
  },
  searchtap: function() {
    var that = this
    wx.request({
      url: getApp().globalData.apiUrl + 'searchList',
      data: {
        openid: getApp().globalData.openid,
        key: getApp().globalData.key
      },
      success: function(res) {
        if (res.statusCode == 200) {
          that.setData({
            adapterSource: res.data
          })
        }
      }
    })
  },
  onLoad: function() {
    getApp().globalData.listPage = this
    var that = this
    var t = 1
    if (!getApp().globalData.mready) {
      t = 2000
    }
    setTimeout(function () {
      wx.request({
        url: getApp().globalData.apiUrl + 'searchList',
        data: {
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            that.setData({
              adapterSource: res.data
            })
          }
        }
      })
      wx.request({
        url: getApp().globalData.apiUrl + 'getList',
        data: {
          k: "w",
          openid: getApp().globalData.openid,
          key: getApp().globalData.key
        },
        success: function(res) {
          if (res.statusCode == 200) {
            if ((Object.keys(res.data)).length > 1) {
              that.setData({
                mlist: res.data
              })
            }
          } else {
            setTimeout(function () {
              wx.request({
                url: getApp().globalData.apiUrl + 'getList',
                data: {
                  k: "w",
                  openid: getApp().globalData.openid,
                  key: getApp().globalData.key
                },
                success: function(res) {
                  if (res.statusCode == 200) {
                    if ((Object.keys(res.data)).length > 1) {
                      that.setData({
                        mlist: res.data
                      })
                    }
                  } else {
                    console.log(res.statusCode)
                    that.setData({
                      e: true
                    })
                  }
                },
                complete: function() {
                  that.setData({
                    loading: false
                  })
                }
              })
            }, 2000)
          }
        },
        complete: function() {
          that.setData({
            loading: false
          })
        }
      })
      if (getApp().globalData.u == 2) {
        that.setData({
          admin: true
        })
      }
    }, t)
  },
  onShow: function() {
    getApp().globalData.listPage = this
  },
  close: function() {
    this.setData({
      e: false
    })
  },
  retry: function() {
    var that = this
    this.setData({
      e: false,
      loading: true
    })
    wx.request({
      url: getApp().globalData.apiUrl + 'getList',
      data: {
        k: "w",
        openid: getApp().globalData.openid,
        key: getApp().globalData.key
      },
      success: function(res) {
        if (res.statusCode == 200 && (Object.keys(res.data)).length > 1) {
          that.setData({
            mlist: res.data
          })
        } else {
          that.setData({
            e: true
          })
        }
      },
      complete: function() {
        that.setData({
          loading: false
        })
      }
    })
    if (getApp().globalData.u == 2) {
      that.setData({
        admin: true
      })
    }
  },
  add: function() {
    wx.navigateTo({
      url: '/pages/operation/operation',
    })
  },
  submit: function(e) {
    wx.navigateTo({
      url: '/pages/listObj/listObj?k=s&t=' + e.detail.value,
    })
  }
})