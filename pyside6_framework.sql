/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80036 (8.0.36)
 Source Host           : localhost:3306
 Source Schema         : rul_framework

 Target Server Type    : MySQL
 Target Server Version : 80036 (8.0.36)
 File Encoding         : 65001

 Date: 10/11/2025 13:45:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for casbin_rule
-- ----------------------------
DROP TABLE IF EXISTS `casbin_rule`;
CREATE TABLE `casbin_rule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `ptype` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v0` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `v5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 628 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of casbin_rule
-- ----------------------------
INSERT INTO `casbin_rule` VALUES (613, 'p', 'admin', 'home', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (614, 'p', 'admin', 'system', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (615, 'p', 'admin', 'component', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (616, 'p', 'admin', 'algorithm', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (617, 'p', 'admin', 'model', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (618, 'p', 'admin', 'system/user', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (619, 'p', 'admin', 'system/menu', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (620, 'p', 'admin', 'system/permission', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (621, 'p', 'admin', 't', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (622, 'p', 'user', 'model', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (623, 'p', 'user', 'system/permission', 'view', NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (624, 'g', 'a', 'admin', NULL, NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (625, 'g', 'b', 'user', NULL, NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (626, 'g', 'admin', 'admin', NULL, NULL, NULL, NULL);
INSERT INTO `casbin_rule` VALUES (627, 'g', 'admin', 'user', NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `route_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `icon` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `parent_id` int NULL DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `route_key`(`route_key` ASC) USING BTREE,
  INDEX `parent_id`(`parent_id` ASC) USING BTREE,
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `menu` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '主页', 'home', 'HOME', NULL, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (2, '系统管理', 'system', 'SETTING', NULL, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (3, '构件管理', 'component', 'FOLDER', NULL, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (4, '算法管理', 'algorithm', 'CODE', NULL, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (5, '模型管理', 'model', 'APPLICATION', NULL, '2025-10-30 06:16:40', '2025-10-31 06:11:28');
INSERT INTO `menu` VALUES (6, '用户管理', 'system/user', 'CONNECT', 2, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (7, '菜单管理', 'system/menu', 'MENU', 2, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `menu` VALUES (8, '权限管理', 'system/permission', 'DEVELOPER_TOOLS', 2, '2025-10-30 06:16:40', '2025-10-30 06:16:40');

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `file_path` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` bigint NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `owner_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `owner_id`(`owner_id` ASC) USING BTREE,
  CONSTRAINT `model_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of model
-- ----------------------------
INSERT INTO `model` VALUES (1, '新建 文本文档.txt', '', 'a\\新建 文本文档.txt', 0, 0, 2, '2025-11-10 05:33:45', '2025-11-10 05:33:45');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_active` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', '2f31f36b627d465bf41f2ae4a1ff62becccd4763acd5d698204c2cf4a2447e1f', 1, '2025-10-30 06:16:40', '2025-10-30 06:16:40');
INSERT INTO `user` VALUES (2, 'a', 'e2f484ee0ab10a7462ee3f835bbcf4b2564000804356c01e629eeb5bf563cec1', 1, '2025-10-30 08:48:52', '2025-10-30 08:48:52');
INSERT INTO `user` VALUES (4, 'b', 'e2f484ee0ab10a7462ee3f835bbcf4b2564000804356c01e629eeb5bf563cec1', 1, '2025-10-30 14:17:26', '2025-10-30 14:17:26');

SET FOREIGN_KEY_CHECKS = 1;
