/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : hostm

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-04-06 18:09:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `hosts`
-- ----------------------------
DROP TABLE IF EXISTS `hosts`;
CREATE TABLE `hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` char(20) NOT NULL,
  `port` int(5) DEFAULT NULL,
  `username` char(20) DEFAULT NULL,
  `password` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of hosts
-- ----------------------------
INSERT INTO `hosts` VALUES ('1', '192.168.20.180', '22', 'root', 'hatVDCA5!');
INSERT INTO `hosts` VALUES ('2', '192.168.20.181', '22', 'root', 'hatVDCA5!');
INSERT INTO `hosts` VALUES ('3', '192.168.20.182', '22', 'root', 'hatVDCA5!');
INSERT INTO `hosts` VALUES ('4', '192.168.20.183', '22', 'root', 'hatVDCA5!');

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(20) NOT NULL,
  `password` char(20) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_type_id` (`type_id`),
  CONSTRAINT `fk_type_id` FOREIGN KEY (`type_id`) REFERENCES `user_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', 'alex', '123456', '1');
INSERT INTO `users` VALUES ('2', 'vincen', '123456', '2');

-- ----------------------------
-- Table structure for `user_to_host`
-- ----------------------------
DROP TABLE IF EXISTS `user_to_host`;
CREATE TABLE `user_to_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `hid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_uid` (`uid`),
  KEY `fk_hid` (`hid`),
  CONSTRAINT `fk_hid` FOREIGN KEY (`hid`) REFERENCES `hosts` (`id`),
  CONSTRAINT `fk_uid` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_to_host
-- ----------------------------
INSERT INTO `user_to_host` VALUES ('1', '1', '1');
INSERT INTO `user_to_host` VALUES ('2', '1', '2');
INSERT INTO `user_to_host` VALUES ('3', '2', '1');
INSERT INTO `user_to_host` VALUES ('4', '2', '2');
INSERT INTO `user_to_host` VALUES ('5', '2', '3');
INSERT INTO `user_to_host` VALUES ('6', '2', '4');

-- ----------------------------
-- Table structure for `user_type`
-- ----------------------------
DROP TABLE IF EXISTS `user_type`;
CREATE TABLE `user_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` char(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_type
-- ----------------------------
INSERT INTO `user_type` VALUES ('1', 'user');
INSERT INTO `user_type` VALUES ('2', 'admin');
