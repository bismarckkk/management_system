# 关于数据库的说明
## logs
用于存储审批记录，这个表比较混乱  
`id` 申请ID  
`time` 申请提交时间  
`openid` 提交人openid  
`operation` 操作类型  
`object` 操作对象  
`name` 对象名  
`num` 操作数目  
`do` 备注  
`verify` 审批状态(0为待审,1为通过,2为退回  
`wis` 位置  
`approver` 审批人  

## main
存储物资大类信息  
`id` 大类ID  
`name` 物资名  
`total` 物资总数  
`useable` 可用物资数  

## members
存储用户信息，注意网页端与微信端用户账号不互通
`openid` 用户openid  
`name` 用户名  
`admin` 是否管理员(1为管理员,0为普通成员)  
`stu_id` 学号  

## object
存储对象详细信息  
`id` 对象ID，前6位为对应大类ID  
`father` 对应大类ID  
`useable` 是否可用  
`wis` 当前位置  
`do` 备注  

## punch
存储签到相关信息  
`id` 签到ID  
`week` 签到周(按周考勤，周为自然周)  
`time` 签到时间  
`openid` 签到人openid  
`name` 签到人姓名  
`location` 签到地点  
`clas` punch为签到,quit为签退,leave为请假  
`worktime` 签到类型不存在工时，签退时记录当天工时(h)，请假记录请假天数