/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50618
Source Host           : localhost:3306
Source Database       : pims

Target Server Type    : MYSQL
Target Server Version : 50618
File Encoding         : 65001

Date: 2014-05-12 00:19:29
*/

SET FOREIGN_KEY_CHECKS=0;
 

-- ----------------------------
-- Records of card
-- ----------------------------
INSERT INTO `card` VALUES ('1', '16777217', '3008894835', '1', '1', '1', null);
INSERT INTO `card` VALUES ('2', '33554434', '3008210723', '2', '2', '1', null);
INSERT INTO `card` VALUES ('3', '67108865', '3009531827', '4', '1', '1', null);
INSERT INTO `card` VALUES ('4', '67108866', '3008532003', '4', '2', '1', null);
INSERT INTO `card` VALUES ('5', '67108867', '3008888707', '4', '3', '1', null);
INSERT INTO `card` VALUES ('6', '67108868', '3008414611', '4', '4', '1', null);
INSERT INTO `card` VALUES ('7', '67108869', '3009874531', '4', '5', '1', null);
INSERT INTO `card` VALUES ('8', '67108870', '3008543843', '4', '6', '1', null);
INSERT INTO `card` VALUES ('9', '67108871', '3008590979', '4', '7', '1', null);
INSERT INTO `card` VALUES ('10', '67108872', '3009594755', '4', '8', '1', null);
INSERT INTO `card` VALUES ('11', '67108873', '3008820803', '4', '9', '1', null);
INSERT INTO `card` VALUES ('12', '50331649', '3008999971', '3', '1', '1', null);
INSERT INTO `card` VALUES ('13', '50331650', '3008985955', '3', '2', '1', null);
INSERT INTO `card` VALUES ('14', '50331651', '3008594435', '3', '3', '1', null);
INSERT INTO `card` VALUES ('15', '83886081', '3009264851', '5', '1', '1', null);
INSERT INTO `card` VALUES ('16', '83886082', '3008547043', '5', '2', '1', null);
INSERT INTO `card` VALUES ('17', '83886082', '3008940051', '5', '2', '1', null);
INSERT INTO `card` VALUES ('18', '83886083', '3009746963', '5', '3', '1', null);
INSERT INTO `card` VALUES ('19', '83886083', '4229575682', '5', '3', '1', null);
INSERT INTO `card` VALUES ('20', '83886081', '3008181619', '5', '1', '1', null);
 

-- ----------------------------
-- Records of employee
-- ----------------------------
INSERT INTO `employee` VALUES ('1', '1', '员工1', '0', '1234567890', null, '2014-04-01 00:04:54', '1', '1', '83886081', null, null);
INSERT INTO `employee` VALUES ('2', '2', '员工2', '0', '1234567890', null, '2014-05-01 00:06:10', '1', '1', '83886082', null, null);
INSERT INTO `employee` VALUES ('3', '3', '员工3', '0', '1234567890', null, '2014-05-10 00:06:46', '1', '1', '83886083', null, null);
 

-- ----------------------------
-- Records of material
-- ----------------------------
INSERT INTO `material` VALUES ('1', '1', '竹荚鱼', '1', '1', '50331649', null);
INSERT INTO `material` VALUES ('2', '2', '沙丁鱼', '1', '1', '50331650', null);
INSERT INTO `material` VALUES ('3', '3', '白身鱼', '1', '1', '50331651', null);
 

-- ----------------------------
-- Records of material_type
-- ----------------------------
INSERT INTO `material_type` VALUES ('1', '1', '原料', '1', null);
INSERT INTO `material_type` VALUES ('2', '2', '半成品', '1', null);
INSERT INTO `material_type` VALUES ('3', '3', '成品', '1', null);
 

-- ----------------------------
-- Records of process
-- ----------------------------
INSERT INTO `process` VALUES ('1', '1', '原料出库', null, '0', '1', '箱', '1', '67108865', null);
INSERT INTO `process` VALUES ('2', '2', '打鳞.领料', null, '1', '0', 'kg', '1', '67108866', null);
INSERT INTO `process` VALUES ('3', '3', '打鳞.交料', '2', '0', '0', 'kg', '1', '67108867', null);
INSERT INTO `process` VALUES ('4', '4', '分身.领料', null, '1', '0', 'kg', '1', '67108868', null);
INSERT INTO `process` VALUES ('5', '5', '分身.交料', '4', '0', '0', 'kg', '1', '67108869', null);
INSERT INTO `process` VALUES ('6', '6', '拼片', null, '0', '0', 'kg', '1', '67108870', null);
INSERT INTO `process` VALUES ('7', '7', '粘粉', null, '0', '1', '盘', '1', '67108871', null);
INSERT INTO `process` VALUES ('8', '8', '包装装箱', null, '0', '1', '箱', '1', '67108872', null);
INSERT INTO `process` VALUES ('9', '9', '成品入库', null, '0', '1', '箱', '1', '67108873', null);
 
-- ----------------------------
-- Records of production
-- ----------------------------
INSERT INTO `production` VALUES ('1', '2', '20', '1', '1', '3', '2014-05-11 01:44:30', '1.00');
INSERT INTO `production` VALUES ('2', '2', '20', '1', '1', '3', '2014-05-11 10:26:56', '1.00');
INSERT INTO `production` VALUES ('3', '1', '20', '1', '1', '2', '2014-05-11 10:35:47', '-641.00');
INSERT INTO `production` VALUES ('4', '1', '20', '1', '1', '2', '2014-05-11 10:35:50', '-641.00');
INSERT INTO `production` VALUES ('5', '1', '20', '1', '1', '2', '2014-05-11 10:39:01', '-641.00');
INSERT INTO `production` VALUES ('6', '1', '20', '1', '1', '2', '2014-05-11 10:39:10', '-641.00');
INSERT INTO `production` VALUES ('7', '1', '20', '1', '1', '2', '2014-05-11 10:39:13', '-641.00');
INSERT INTO `production` VALUES ('8', '1', '20', '1', '1', '2', '2014-05-11 10:39:19', '-641.00');
INSERT INTO `production` VALUES ('9', '1', '20', '1', '1', '2', '2014-05-11 10:39:25', '-641.00');
INSERT INTO `production` VALUES ('10', '1', '20', '1', '1', '2', '2014-05-11 10:41:48', '-641.00');
INSERT INTO `production` VALUES ('11', '1', '20', '1', '1', '2', '2014-05-11 10:41:51', '-641.00');
INSERT INTO `production` VALUES ('12', '1', '20', '1', '1', '2', '2014-05-11 10:41:54', '-641.00');
INSERT INTO `production` VALUES ('13', '1', '20', '1', '1', '2', '2014-05-11 10:45:03', '-641.00');
INSERT INTO `production` VALUES ('14', '1', '20', '1', '1', '2', '2014-05-11 10:45:06', '-641.00');
 

-- ----------------------------
-- Records of report_class
-- ----------------------------
 

-- ----------------------------
-- Records of report_employee
-- ----------------------------

-- ----------------------------
-- Table structure for `salary_count_config`
-- ----------------------------
 

-- ----------------------------
-- Records of salary_count_config
-- ----------------------------
 

-- ----------------------------
-- Records of terminal
-- ----------------------------
INSERT INTO `terminal` VALUES ('1', '1', '计重前终端', '1', '1', '192.168.127.11', '192.168.127.111', null, '1', '2');
INSERT INTO `terminal` VALUES ('2', '2', '计重后终端', '1', '1', '192.168.127.12', '192.168.127.112', null, '1', '3');
INSERT INTO `terminal` VALUES ('3', '3', '中间计重终端', '1', '2', '192.168.127.13', '192.168.127.113', null, '1', '6');
INSERT INTO `terminal` VALUES ('4', '4', '计数终端1', '2', '3', '192.168.127.14', null, null, '1', '1');
 

-- ----------------------------
-- Records of workclass
-- ----------------------------
INSERT INTO `workclass` VALUES ('1', '1', '开始', '0', '1', '1', null);
INSERT INTO `workclass` VALUES ('2', '2', '结束', '1', '1', '2', null);
 

-- ----------------------------
-- Records of workgroup
-- ----------------------------
INSERT INTO `workgroup` VALUES ('1', '计重考核组1', null, '1');
INSERT INTO `workgroup` VALUES ('2', '中间计重组', null, '1');
INSERT INTO `workgroup` VALUES ('3', '计数组1', null, '1');
 

-- ----------------------------
-- Records of workshift
-- ----------------------------
INSERT INTO `workshift` VALUES ('20', '1', '1', '2014-05-11 01:40:48');
INSERT INTO `workshift` VALUES ('21', '2', '1', '2014-05-11 01:41:03');
INSERT INTO `workshift` VALUES ('22', '1', '12', '2014-05-11 01:41:33');
INSERT INTO `workshift` VALUES ('23', '2', '12', '2014-05-11 01:41:33');
INSERT INTO `workshift` VALUES ('24', '1', '4', '2014-05-11 01:41:51');
INSERT INTO `workshift` VALUES ('25', '1', '9', '2014-05-11 01:43:45');
INSERT INTO `workshift` VALUES ('26', '1', '2', '2014-05-11 01:49:42');
INSERT INTO `workshift` VALUES ('27', '2', '1', '2014-05-11 01:50:54');
INSERT INTO `workshift` VALUES ('28', '2', '1', '2014-05-11 10:26:53');
INSERT INTO `workshift` VALUES ('29', '2', '1', '2014-05-11 10:30:17');
INSERT INTO `workshift` VALUES ('30', '2', '1', '2014-05-11 10:35:37');
INSERT INTO `workshift` VALUES ('31', '2', '1', '2014-05-11 10:38:33');
INSERT INTO `workshift` VALUES ('32', '2', '1', '2014-05-11 10:41:39');
INSERT INTO `workshift` VALUES ('33', '2', '1', '2014-05-11 10:44:50');
INSERT INTO `workshift` VALUES ('34', '2', '1', '2014-05-11 10:44:53');
 

-- ----------------------------
-- Records of workshop
-- ----------------------------
INSERT INTO `workshop` VALUES ('1', '罐头车间', null);
