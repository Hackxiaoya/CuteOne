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

 Date: 07/04/2019 18:04:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cuteone_auth_group
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_auth_group`;
CREATE TABLE `cuteone_auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `auth_group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `price` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0.00',
  `update_time` datetime(0) NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'auth_group' ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '权限规则表' ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cuteone_config
-- ----------------------------
INSERT INTO `cuteone_config` VALUES (1, 'username', '后台管理员用户名', 'admin', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (2, 'password', '后台管理员密码', '60a25dd28e65a2c6df9e3b2650c926e6', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (3, 'toggle_web_site', '站点开关', '1', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (4, 'web_site', '域名地址', '', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (5, 'web_site_title', '网站标题', 'CuteOne 网盘系统', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (6, 'web_site_logo', '网站LOGO', '/static/uploads/logo.png', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (7, 'web_site_description', 'SEO描述', 'SEO的描述', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (8, 'web_site_keyword', 'SEO关键字', 'SEO的关键字', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (9, 'web_site_copyright', '版权信息', 'Copyright © CuteOne All rights reserved.', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (10, 'web_site_icp', '网站备案号', '<a href=\"https://github.com/Hackxiaoya/CuteOne\">CuteOne</a>', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (11, 'web_site_statistics', '站点统计', '', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (12, 'page_number', '列表条数', '10', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (13, 'search_type', '搜索类型', '0', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (14, 'web_site_background', '背景图', 'http://ww1.sinaimg.cn/large/71c534f0ly1fw9tw14zb3j21hc0u01e4.jpg', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (15, 'is_users', '是否开启用户模块', '0', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (16, 'is_music', '音乐播放器', '0', '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (17, 'files_disk_id', '用户默认存储盘', NULL, '0001-01-01 00:00:00', '0001-01-01 00:00:00');
INSERT INTO `cuteone_config` VALUES (18, 'files_uploads', '是否开启用户上传', '0', '0001-01-01 00:00:00', '0001-01-01 00:00:00');

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘管理表' ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '网盘列表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_files
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_files`;
CREATE TABLE `cuteone_files`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `disk_id` int(11) NOT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `size` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `file` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `files_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT 0,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'Files' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_files_disk
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_files_disk`;
CREATE TABLE `cuteone_files_disk`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `client_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用ID，client_id',
  `client_secret` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '应用机密，client_secret',
  `token` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '应用Token',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'files disk' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_funds
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_funds`;
CREATE TABLE `cuteone_funds`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(1) NOT NULL DEFAULT 0,
  `update_time` datetime(0) NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '资金列表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_task
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_task`;
CREATE TABLE `cuteone_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drive_id` int(11) NULL DEFAULT NULL COMMENT '驱动id',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路径',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '状态',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务管理表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cuteone_users
-- ----------------------------
DROP TABLE IF EXISTS `cuteone_users`;
CREATE TABLE `cuteone_users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '登录邮箱',
  `mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '手机号',
  `avatar` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户头像，相对于uploads/avatar目录',
  `sex` smallint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '性别；0：保密，1：男；2：女',
  `birthday` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '生日',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '个人描述',
  `register_ip` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '注册IP',
  `login_num` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '0' COMMENT '登录次数',
  `last_login_ip` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '最后登录ip',
  `last_login_time` datetime(0) NULL DEFAULT '0001-01-01 00:00:00' COMMENT '最后登录时间',
  `score` int(11) UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户积分',
  `group` int(3) NULL DEFAULT 0 COMMENT '等级',
  `files_disk_id` int(3) NULL DEFAULT 0,
  `status` int(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '用户状态 0：禁用； 1：正常 ；',
  `reg_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '注册时间',
  `update_time` datetime(0) NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'Users' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
