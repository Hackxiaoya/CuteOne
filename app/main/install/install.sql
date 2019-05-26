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

 Date: 26/05/2019 19:44:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
-- ----------------------------
-- Table structure for cuteone_auth_group
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_auth_group`;
CREATE TABLE `cuteone_auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '标题',
  `auth_group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '权限ID数组',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `price` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0.00' COMMENT '价格',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '权限组表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_auth_rule
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_auth_rule`;
CREATE TABLE `cuteone_auth_rule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `drive_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '驱动ID',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路径',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `login_hide` int(1) NULL DEFAULT 0 COMMENT '登陆显示',
  `status` int(1) NOT NULL DEFAULT 1 COMMENT '是否有效(0:无效,1:有效)',
  `update_time` datetime(0) NULL DEFAULT '0001-01-01 00:00:00' COMMENT '更新时间',
  `create_time` datetime(0) NULL DEFAULT '0001-01-01 00:00:00' COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '权限规则表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_config
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_config`;
CREATE TABLE `cuteone_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置名称',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置说明',
  `value` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '配置值',
  `update_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '更新时间',
  `create_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cuteone_config
-- ----------------------------
INSERT INTO `cuteone_config` VALUES (1, 'username', '后台管理员用户名', 'admin', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (1, 'username', '后台管理员用户名', 'admin', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (2, 'password', '后台管理员密码', '60a25dd28e65a2c6df9e3b2650c926e6', '0001-01-01 00:00:00', '2019-03-15 12:05:40');
INSERT INTO `cuteone_config` VALUES (3, 'toggle_web_site', '站点开关', '1', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (4, 'web_site', '域名地址', '', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (5, 'web_site_title', '网站标题', 'CuteOne 网盘系统', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (6, 'web_site_logo', '网站LOGO', '/static/uploads/logo.png', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (7, 'web_site_description', 'SEO描述', 'SEO的描述', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (8, 'web_site_keyword', 'SEO关键字', 'SEO的关键字', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (9, 'web_site_copyright', '版权信息', 'Copyright © CuteOne All rights reserved.', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (10, 'web_site_icp', '网站备案号', '<a href=\"https://github.com/Hackxiaoya/CuteOne\">CuteOne</a>', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (11, 'web_site_statistics', '站点统计', '', '2019-04-09 00:34:28', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (12, 'page_number', '列表条数', '30', '2019-05-24 17:23:17', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (13, 'search_type', '搜索类型', '0', '2019-05-24 17:23:17', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (14, 'web_site_background', '背景图', 'http://ww1.sinaimg.cn/large/71c534f0ly1fw9tw14zb3j21hc0u01e4.jpg', '2019-05-24 17:23:17', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (15, 'is_music', '音乐播放器', '0', '2019-05-24 17:23:17', '0001-01-01 00:00:00');

-- ----------------------------
-- Table structure for cuteone_disk
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_disk`;
CREATE TABLE `cuteone_disk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drive_id` int(11) NOT NULL COMMENT '驱动ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标题',
  `types` int(1) NOT NULL DEFAULT 1 COMMENT '网盘类型：1 onedrive',
  `client_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用ID，client_id',
  `client_secret` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用机密，client_secret',
  `token` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '应用Token',
  `chief` int(1) NULL DEFAULT 0 COMMENT '是否是主盘，1为主盘，0为从盘',
  `status` int(1) NULL DEFAULT 1 COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘列表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_drive
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_drive`;
CREATE TABLE `cuteone_drive`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '网盘标题',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '网盘描述',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘管理表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_hooks
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_hooks`;
CREATE TABLE `cuteone_hooks`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '钩子名称',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '钩子描述',
  `source` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '钩子来源于什么模块或插件',
  `type` int(1) NOT NULL DEFAULT 0 COMMENT '钩子类型，0模型，1插件',
  `method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '钩子方法函数名',
  `position` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '钩子位置',
  `status` int(1) NOT NULL DEFAULT 1 COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '钩子表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_menu
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_menu`;
CREATE TABLE `cuteone_menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NULL DEFAULT NULL COMMENT '父级ID',
  `postion` int(1) NOT NULL DEFAULT 0 COMMENT '位置，0是前端 1是后台',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'url',
  `icon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图标',
  `top_nav` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '顶级导航',
  `activity_nav` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '二级导航',
  `type` int(1) NOT NULL DEFAULT 0 COMMENT '类型0是自定义，1是网盘驱动，2是模型，3是插件',
  `type_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '模型或者插件的name',
  `activate` int(1) NOT NULL DEFAULT 0 COMMENT '是否默认首页显示驱动，1是 0不是',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '密码',
  `sort` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '排序，越大越靠前',
  `status` int(1) NOT NULL DEFAULT 1 COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 402 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_model
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_model`;
CREATE TABLE `cuteone_model`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '唯一名称',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `config` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '配置',
  `status` int(1) NOT NULL DEFAULT 0 COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '模型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_plugin
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_plugin`;
CREATE TABLE `cuteone_plugin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '唯一标识',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `config` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '配资',
  `status` int(1) NOT NULL DEFAULT 0 COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '插件表' ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for cuteone_uploads_list
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_uploads_list`;
CREATE TABLE `cuteone_uploads_list`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drive_id` int(11) NULL DEFAULT NULL COMMENT '驱动id',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路径',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '后台文件上传表' ROW_FORMAT = Dynamic;

