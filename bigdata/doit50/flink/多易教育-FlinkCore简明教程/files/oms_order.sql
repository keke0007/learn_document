/*
Navicat MySQL Data Transfer

Source Server         : doitedu
Source Server Version : 50738
Source Host           : doitedu:3306
Source Database       : rtmk

Target Server Type    : MYSQL
Target Server Version : 50738
File Encoding         : 65001

Date: 2023-06-17 19:46:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for oms_order
-- ----------------------------
DROP TABLE IF EXISTS `oms_order`;
CREATE TABLE `oms_order` (
  `id` int(11) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `total_amount` decimal(10,0) DEFAULT NULL,
  `pay_amount` decimal(10,0) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `payment_time` timestamp NULL DEFAULT NULL,
  `delivery_time` timestamp NULL DEFAULT NULL,
  `confirm_time` timestamp NULL DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of oms_order
-- ----------------------------
INSERT INTO `oms_order` VALUES ('3', '1', '140', '120', '2023-06-16 09:02:00', '2023-06-17 10:02:10', null, null, 'a', '2023-06-17 10:02:10');
INSERT INTO `oms_order` VALUES ('4', '1', '140', '120', '2023-06-17 09:22:00', '2023-06-17 10:03:10', null, null, 'a', '2023-06-17 10:03:10');
INSERT INTO `oms_order` VALUES ('5', '1', '140', '120', '2023-06-17 10:04:10', '2023-06-17 10:05:10', null, null, 'a', '2023-06-17 10:04:10');
