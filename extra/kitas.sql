-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: kitas
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cust_activity`
--

DROP TABLE IF EXISTS `cust_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cust_activity` (
  `cust_id` int(11) NOT NULL,
  `rec_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `cust_id` (`cust_id`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `cust_activity_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `cust_activity_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `recipes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cust_activity`
--

LOCK TABLES `cust_activity` WRITE;
/*!40000 ALTER TABLE `cust_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `cust_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cust_fav`
--

DROP TABLE IF EXISTS `cust_fav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cust_fav` (
  `cust_id` int(11) NOT NULL,
  `rec_id` int(11) NOT NULL,
  `favourite` tinyint(1) DEFAULT NULL,
  `bookmark` tinyint(1) DEFAULT NULL,
  KEY `cust_id` (`cust_id`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `cust_fav_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `cust_fav_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `recipes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cust_fav`
--

LOCK TABLES `cust_fav` WRITE;
/*!40000 ALTER TABLE `cust_fav` DISABLE KEYS */;
/*!40000 ALTER TABLE `cust_fav` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cust_ingredients`
--

DROP TABLE IF EXISTS `cust_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cust_ingredients` (
  `cust_id` int(11) DEFAULT NULL,
  `ingr_id` int(11) DEFAULT NULL,
  `qty` varchar(40) DEFAULT NULL,
  KEY `cust_id` (`cust_id`),
  KEY `ingr_id` (`ingr_id`),
  CONSTRAINT `cust_ingredients_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `cust_ingredients_ibfk_2` FOREIGN KEY (`ingr_id`) REFERENCES `ingredients` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cust_ingredients`
--

LOCK TABLES `cust_ingredients` WRITE;
/*!40000 ALTER TABLE `cust_ingredients` DISABLE KEYS */;
/*!40000 ALTER TABLE `cust_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'admin','admin@kitas.com','admin');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(4,'auth','permission'),(3,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-10-02 14:53:56'),(2,'auth','0001_initial','2017-10-02 14:54:15'),(3,'admin','0001_initial','2017-10-02 14:54:21'),(4,'admin','0002_logentry_remove_auto_add','2017-10-02 14:54:22'),(5,'contenttypes','0002_remove_content_type_name','2017-10-02 14:54:24'),(6,'auth','0002_alter_permission_name_max_length','2017-10-02 14:54:24'),(7,'auth','0003_alter_user_email_max_length','2017-10-02 14:54:25'),(8,'auth','0004_alter_user_username_opts','2017-10-02 14:54:25'),(9,'auth','0005_alter_user_last_login_null','2017-10-02 14:54:26'),(10,'auth','0006_require_contenttypes_0002','2017-10-02 14:54:26'),(11,'auth','0007_alter_validators_add_error_messages','2017-10-02 14:54:26'),(12,'auth','0008_alter_user_username_max_length','2017-10-02 14:54:27'),(13,'sessions','0001_initial','2017-10-02 14:54:29');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('32ijnc3dlbl48m18bnwtzgqquok9l2yv','NzJiMDI5MTUwOWQ5NmYxODU3ZTI3YTQzZDdjYzNhODgzZGJmNDBhYzp7InVzZXIiOiJhZG1pbiIsImlkIjoxfQ==','2017-10-20 11:59:14.737980'),('uykw7rc5shy9g5k1kfnolbrqwlrf57ov','Njk2MzY3MGU0M2U2MjkxZDQxYTJhZjdkZDgzMGRlNGY5OWJjZTU2MTp7InVzZXIiOm51bGx9','2017-10-16 14:54:59.931339');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingr_categories`
--

DROP TABLE IF EXISTS `ingr_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingr_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingr_categories`
--

LOCK TABLES `ingr_categories` WRITE;
/*!40000 ALTER TABLE `ingr_categories` DISABLE KEYS */;
INSERT INTO `ingr_categories` VALUES (1,'Dairy'),(2,'Vegetables'),(3,'Fruits'),(4,'Meats'),(5,'Grains'),(6,'Spices'),(1000,'Others');
/*!40000 ALTER TABLE `ingr_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_english` varchar(40) DEFAULT NULL,
  `name_hindi` varchar(40) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category` (`category`),
  CONSTRAINT `ingredients_ibfk_1` FOREIGN KEY (`category`) REFERENCES `ingr_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (1,'wheat flour','aata',5),(2,'flour','maida',5),(3,'ghee','ghee',1000),(4,'oil',NULL,1000),(5,'puffed rice','bhel',1000),(6,'potato',NULL,2),(7,'onion',NULL,2),(8,'tomato',NULL,2),(9,'coriander leaves',NULL,2),(10,'cumin',NULL,6),(11,'green chillies',NULL,6),(12,'black pepper',NULL,6),(13,'tamarind',NULL,6),(14,'jaggery',NULL,6),(15,NULL,'besan',5),(16,'red pepper',NULL,6),(17,'salt',NULL,6),(18,NULL,'garam masala',6),(19,'paprika',NULL,6),(20,'spinach',NULL,2);
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_categories`
--

DROP TABLE IF EXISTS `rec_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_categories`
--

LOCK TABLES `rec_categories` WRITE;
/*!40000 ALTER TABLE `rec_categories` DISABLE KEYS */;
INSERT INTO `rec_categories` VALUES (1,'Breads'),(2,'Snacks'),(3,'Vegetables'),(4,'Lentils'),(5,'Rice'),(6,'Fish'),(7,'Chicken'),(8,'Lamb and Beef'),(9,'Desserts'),(10,'This and That'),(1000,'Others');
/*!40000 ALTER TABLE `rec_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_ingredients`
--

DROP TABLE IF EXISTS `rec_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_ingredients` (
  `rec_id` int(11) DEFAULT NULL,
  `qty_string` varchar(40) DEFAULT NULL,
  `ingr_string` varchar(60) DEFAULT NULL,
  `qty` varchar(40) DEFAULT NULL,
  `ingr_id` int(11) DEFAULT NULL,
  KEY `ingr_id` (`ingr_id`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `rec_ingredients_ibfk_1` FOREIGN KEY (`ingr_id`) REFERENCES `ingredients` (`id`),
  CONSTRAINT `rec_ingredients_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `recipes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_ingredients`
--

LOCK TABLES `rec_ingredients` WRITE;
/*!40000 ALTER TABLE `rec_ingredients` DISABLE KEYS */;
INSERT INTO `rec_ingredients` VALUES (1,'1 cup','Whole wheat flour (or 1/3 white + 2/3 whole wheat)','150g',1),(1,'1/2 cup','Water',NULL,NULL),(2,'1 cup','Whole wheat flour','150g',1),(2,NULL,'Ghee',NULL,3),(2,NULL,'Water',NULL,NULL),(3,'1 packet','Bhel mix or Sev',NULL,4),(3,'2','2 Mashed boiled potatoes (mashed coarsely and then salted)','2',6),(3,'1/2 cup','Chopped fresh coriander leaves (a.k.a Chinese parsley)','75g',9),(3,'3 tsp','Freshly roasted and ground cumin','15g',10),(3,'to taste','Green chilies',NULL,11),(3,'1-2 tsp','Freshly ground black pepper','5g',12),(3,'to taste','Tamarind',NULL,13),(3,'to taste','Jaggery (or Brown Sugar)',NULL,14),(3,'1 cup','Chopped onions.','150g',7),(4,'1/2 cup','Besan','75g',15),(4,'1 cup','Warm water',NULL,NULL),(4,'1/4 tsp','Red pepper','1g',16),(4,'3/4 tsp','Salt','3g',17),(4,'1/2 tsp','Garam Masala','2g',18),(4,'(optional)','paprika',NULL,19),(4,'1','1 Small onion','1',7),(4,'1','1 Potato','1',6),(4,NULL,'A few spinach leaves ',NULL,20),(4,NULL,'Oil for deep frying',NULL,4);
/*!40000 ALTER TABLE `rec_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  `directions` varchar(2000) DEFAULT NULL,
  `cust_id` int(11) DEFAULT NULL,
  `time_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `servings` varchar(40) DEFAULT NULL,
  `prep_time` varchar(40) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cust_id` (`cust_id`),
  KEY `category` (`category`),
  CONSTRAINT `recipes_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `recipes_ibfk_2` FOREIGN KEY (`category`) REFERENCES `rec_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES (1,'CHAPATI (PHULKA)','Put flour in a large bowl with half the water. Blend the two together until it holds.  Beat and knead well until it forms a compact ball.<br><br>Knead dough until it is smooth and elastic.  Set aside for 30 minutes.<br><br>Knead and divide dough into 4 to 6 parts.  Roll each ball into a tortilla like flat, about 1/8\" thick.  Heat an ungreased skillet. <br><br>Put phulka on it, and let it cook for about 1 minute (The top should just start to look dry and small bubbles should just start to form). <br><br>Turn and cook the second side for 2/3 minutes until small bubbles form. <br><br>Turn again and cook the first side pressed lightly with a towel.  It should puff.  Serve warm (maybe slightly buttered).<br> ',1,'2017-10-05 18:13:27','serves 4, 1-2 for each',NULL,1),(2,'PARATHA','Make chappati dough.  Divide into 6 parts and make balls.  Flatten and roll each. <br><br>Spread ghee over them and fold.  Roll again. <br><br>Heat the paratha on a griddle like you would a chappati, but spread some ghee over the top side.  Turn and spread ghee on the other side. Fry until the bottom is crisp and golden, then turn and fry the remaining side. <br><br>Repeat with all six. <br><br>Serve at once, since they lose crispness if stored.<br>',1,'2017-10-05 18:13:27',NULL,NULL,1),(3,'BHEL','First boil the potatoes, mash them, salt them, and add pepper to taste. Add some coriander leaves too. <br><br>Roast the cumin and grind it.<br><br>Dissolve about 4 Tbsp of tamarind concentrate in 1 cup of hot water, and let it simmer and thicken gradually.  Dissolve the jaggery (or sugar) until the sauce becomes tart and slightly sweet.  (You may add some salt<br>and ground red paprika, if you want to.) The sauce should be of a consistency slightly thinner than maple syrup.  Pour into a serving container (like a creamer).  Mix the puffed rice and sev/bhel mix in a large bowl. <br><br>On a plate, serve the rice-bhel mixture, add the potatoes, then the onions, chilies, and then dust the cumin powder over it.  Next pour on the sauce and top with the coriander garnish. (Add salt/pepper to<br>taste). <br><br>Mix the ingredients on the plate and eat. <br>',1,'2017-10-05 18:13:27',NULL,NULL,2),(4,'PAKORAS (SAVORY FRITTERS)','In a bowl put the besan and half the water, and stir until it becomes a thick batter.  Beat hard for 5 minutes.  gradually add the rest of the water, and leave to swell for 30 minutes.  Add salt, pepper and Garam Masala and beat again. <br><br>Wash peel and slice the onion and potatoes.  Wash and pat dry the spinach leaves. <br><br>Heat oil until smoking hot, dip the vegetables in the batter and deep fry until golden brown. <br><br>Serve hot. <br>',1,'2017-10-05 18:13:27',NULL,NULL,2);
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-06 17:40:33
