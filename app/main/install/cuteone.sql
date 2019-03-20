/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : cuteone

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 20/03/2019 22:57:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cuteone_auth_rule
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_auth_rule`;
CREATE TABLE `cuteone_auth_rule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `depend_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '类型',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图标',
  `is_menu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '是否显示菜单',
  `sort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否有效(0:无效,1:有效)',
  `update_time` datetime(0) NULL DEFAULT '0001-01-01 00:00:00' COMMENT '更新时间',
  `create_time` datetime(0) NULL DEFAULT '0001-01-01 00:00:00' COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '权限规则表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_config
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_config`;
CREATE TABLE `cuteone_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置名称',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置说明',
  `value` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '配置值',
  `create_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cuteone_config
-- ----------------------------
INSERT INTO `cuteone_config` VALUES (1, 'username', '后台管理员用户名', 'admin', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (1, 'username', '后台管理员用户名', 'admin', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (2, 'password', '后台管理员密码', '60a25dd28e65a2c6df9e3b2650c926e6', '0001-01-01 00:00:00', '2019-03-15 12:05:40');
INSERT INTO `cuteone_config` VALUES (3, 'toggle_web_site', '站点开关', '1', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (4, 'web_site', '域名地址', '', '0001-01-01 00:00:00', '2019-03-18 20:37:17');
INSERT INTO `cuteone_config` VALUES (5, 'web_site_title', '网站标题', 'CuteOne 网盘系统', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (6, 'web_site_logo', '网站LOGO', NULL, '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (7, 'web_site_description', 'SEO描述', 'SEO的描述', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (8, 'web_site_keyword', 'SEO关键字', 'SEO的关键字', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (9, 'web_site_copyright', '版权信息', 'Copyright © ******有限公司 All rights reserved.', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (10, 'web_site_icp', '网站备案号', '', '0001-01-01 00:00:00', '2019-03-17 17:44:45');
INSERT INTO `cuteone_config` VALUES (11, 'web_site_statistics', '站点统计', '', '0001-01-01 00:00:00', '2019-03-17 17:44:45');

-- ----------------------------
-- Table structure for cuteone_drive
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_drive`;
CREATE TABLE `cuteone_drive`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '网盘标题',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '网盘描述',
  `activate` int(1) NOT NULL DEFAULT 0 COMMENT '是否默认首页显示驱动，1是 0不是',
  `sort` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '排序，越小越靠前',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘管理表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_drive_list
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_drive_list`;
CREATE TABLE `cuteone_drive_list`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drive_id` int(11) NOT NULL COMMENT '驱动ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标题',
  `client_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用ID，client_id',
  `client_secret` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用机密，client_secret',
  `token` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '应用Token',
  `chief` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '0' COMMENT '是否是主盘，1为主盘，0为从盘',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '1' COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘列表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
