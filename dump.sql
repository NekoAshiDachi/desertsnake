-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: desertsnake$shotokan_scholar
-- ------------------------------------------------------
-- Server version	5.6.40-log

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
-- Table structure for table `glossary`
--

DROP TABLE IF EXISTS `glossary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `glossary` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `word` varchar(25) DEFAULT NULL,
  `translation` varchar(25) DEFAULT NULL,
  `kanji` varchar(25) DEFAULT NULL,
  `type` varchar(25) DEFAULT NULL,
  `notes` text,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `glossary`
--

LOCK TABLES `glossary` WRITE;
/*!40000 ALTER TABLE `glossary` DISABLE KEYS */;
INSERT INTO `glossary` VALUES (1,'Dōjō','Training Hall','道場','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(2,'Sensei','Instructor','先生','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(3,'Senpai','Senior Student; Mentor','先輩','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(4,'Kōhai','Junior Student; Mentee','後輩','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(5,'Rei','Bow','礼','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(6,'Migi','Right','右','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(7,'Kamae','Base; Posture; Waiting or','構え','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(8,'Mawatte','Turn','回って','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(9,'Gi','Karate uniform','着; 衣','GENERAL','This is usualy short fort the correct form \"Karate-gi\"\"','2020-02-02 18:52:30','2020-02-02 18:52:30'),(10,'Kime','Focus','決め','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(11,'Kihon','Basic techniques; Fundame','基本','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(12,'Kumite','Sparring','組手','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(13,'Jōdan','Upper Level','上段','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(14,'Chūdan','Middle body','中段','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(15,'Gedan','Lower body','下段','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(16,'Dojo Kun','Dojo code','道場訓','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(17,'Seiza','Proper sitting','正座','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(18,'Yoi','Ready','用意','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(19,'Hidari','Left','左','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(20,'Hajime','Start/begin','初め; 始め','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(21,'Yame','Finish/stop','止め','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(22,'Obi','Belt; Sash','帯','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(23,'Kiai','Martial shout','気合','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(24,'Kata','Form','型; 形','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(25,'Zanshin','Martial state of mind; Aw','残心','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(26,'Osu','Respectful greeting;','押忍','GENERAL','Also pronounced \"Oss\"; Multiple meanings depending on the context, usually with the connotation of \"I aknowledge\".','2020-02-02 18:52:30','2020-02-02 18:52:30'),(27,'Dan','Level; Grade; Rank','段','GENERAL',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(28,'Heikō-dachi','Parallel stance','平行立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(29,'Musubi-dachi','Connected stance','結び立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(30,'Kiba-dachi','Horse-ridding stance','騎馬立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(31,'Kōkutsu-dachi','Back stance','閉足立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(32,'Heisoku-dachi','Feet together stance','閉足立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(33,'Zenkutsu-dachi','Front stance','前屈立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(34,'Shiko-dachi','Square stance','四股立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(35,'Hachiji-dachi',NULL,'八字立','TACHI','Used interchangeably with Shizentai; shaped like number eight (八).','2020-02-02 18:52:30','2020-02-02 18:52:30'),(36,'Shizentai','Natural stance','自然体','TACHI','Used interchangeably with Hachiji-dachi','2020-02-02 18:52:30','2020-02-02 18:52:30'),(37,'Nekoashi-dachi','Cat foot stance','猫足立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(38,'Fudō-dachi','Immovable stance','不動立','TACHI','Used interchangeably with Sōchin-dachi','2020-02-02 18:52:30','2020-02-02 18:52:30'),(39,'Sōchin-dachi','Immovable stance','壯鎭立','TACHI','Used interchangeably with Fudō-dachi; from the Sōchin kata','2020-02-02 18:52:30','2020-02-02 18:52:30'),(40,'Sanchin-dachi','Three Battles stance','三戦立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(41,'Hangetsu-dachi','Halfmoon stance','半月立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(42,'Moto-dachi','Foundational stance','基立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(43,'Kosa-dachi','Crossing stance','交差立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(44,'Renoji-dachi','Character レ [Re] stance','レの字立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(45,'Tsuruashi-dachi','Crane-foot stance','鶴足立','TACHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(46,'Jōdan uke','Upper level blocks','上段受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(47,'Hirate sukui age uke','Scooping palm block','平手掬い揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(48,'Jōhō uke','Upward blocks','上方受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(49,'Age uke','Rising block','揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(50,'Kakutō uke','Crane head block','鶴頭受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(51,'Keitō uke','Chicken head block','鶏頭受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(52,'Age teishō uke','Rising palm heel block','揚げ底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(53,'Shō age uke','Rising palm block','掌揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(54,'Shutō jūji uke','Sword hand cross block','手刀十字受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(55,'Magetori barai uke','Grabbing topknot block','髷取払受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(56,'Morote koken uke','Two-handed back of wrist ','諸手上段弧拳受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(57,'Ryō ko uke','Two-handed arc block','両弧受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(58,'Morote age uke','Double rising block','諸手揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(59,'Ryō ken jūji uke','Cross block with fists','両拳十字受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(60,'Morote teishō uke','Double palm heel block','諸手底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(61,'Shoken sukui age uke','First knuckle fist scoopi','初拳掬い揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(62,'Taihineri ko uke','Body twisting arc block','体捻り弧受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(63,'Naihō uke','Inward blocks','内方受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(64,'Uchi ude uke','Inward forearm block','內腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(65,'Mawashi teishō uke','Roundhouse palm heel bloc','回し底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(66,'Te nagashi uke','Flowing hand block','手流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(67,'Mawashi keitō uke','Roundhouse chicken head b','回し鶏頭受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(68,'Morote tsukami uke','Two-handed grasping block','諸手掴み受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(69,'Rasen uke','Spiral block','螺旋受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(70,'Ryō wan hasami uke','Scissor block','両腕鋏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(71,'Tekubi yoko uchi barai','Side-sweeping block with ','手首上段横内払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(72,'Gaihō uke','Outward blocks','外方受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(73,'Soto ude uke','Outward forearm block','外腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(74,'Shutō uke','Sword hand block','手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(75,'Kake shutō uke','Hooking sword hand block','掛け手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(76,'Tate shutō uke','Vertical sword hand block','縦手刀受え','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(77,'Haishu uke','Back of hand block','背手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(78,'Gaiwan nagashi uke','Outer forearm block','外腕流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(79,'Haiwan nagashi uke','Back of forearm block','背腕流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(80,'Naiwan nagashi uke','Inner forearm block','内腕流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(81,'Morote uke','Augmented block','諸手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(82,'Sokumen awase uke','Side combined block','側面合せ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(83,'Oshi uke','Pushing block','押し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(84,'Yama uke','Mountain block','山受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(85,'Morote tenshō uke','Double rolling hand block','諸手転掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(86,'Wari uke','Split block','割受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(87,'Morote nagashi uke','Augmented flowing block','諸手流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(88,'Seiryūtō awase uke','Combined ox-jaw hand bloc','青竜刀合せ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(89,'Ryō shō yoko barai','Side block','両掌横払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(90,'Ryō ken sokumen uke','Block to side with both f','両拳側面受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(91,'Kaishu haiwan uke','Open hand back hand block','開手背腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(92,'Yoko uke','Side block','横受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(93,'Ryōte uke','Two-handed block','両手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(94,'Tsuki uke','Punch block','突き受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(95,'Haishu sasae uke','Supported backhand block','背手支え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(96,'Jōdan haiwan uke','Back of arm block','上段背腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(97,'Tome uke','Stopping block','止め受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(98,'Morote kake uke','Augmented hooking block','上段諸手掛け受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(99,'Ryō ude ni yoru burokku','Block with two arms','両腕によるブロック','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(100,'Otoshi uke','Dropping blocks','落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(101,'Otoshi ude uke','Dropping forearm','落とし腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(102,'Maeude deai osae uke','Forearm pressing','前腕出会い押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(103,'Otoshi teishō uke','Dropping palm heel block','落とし底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(104,'Te osae uke','Pressing hand block','手押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(105,'Seiryūtō uke','Ox-jaw hand block','青竜刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(106,'Tekubi kake uke','Bent wrist block','手首掛受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(107,'Tettsui otoshi uke','Hammerfist dropping block','鉄槌落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(108,'Hai tekubi osae uke','Pressing block with','背手首押さえ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(109,'Morote tettsui otoshi uke','Double hammerfist droppin','諸手鉄槌落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(110,'Morote otoshi ude uke','Double arm middle level d','諸手落とし腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(111,'Ryō shō osae uke','Two-handed pressing block','両掌押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(112,'Chūdan otoshi uke','Middle level dropping blo','中段落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(113,'Haishu otoshi uke','Back of hand dropping blo','背手落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(114,'Haishu osae uke','Back of hand pressing blo','背手押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(115,'Otoshi nekote uke','Dropping cat-paw block','落とし猫手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(116,'Naihō uke','Inward blocks','内方受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(117,'Uchi ude uke','Inward forearm block','內腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(118,'Mawashi teishō uke','Roundhouse palm heel bloc','回し底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(119,'Te nagashi uke','Flowing hand block','手流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(120,'Morote tsukami uke','Two-handed grasping block','諸手掴み受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(121,'Mawashi empi uke','Roundhouse elbow block','回し猿臂受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(122,'Hirabasami uke','Scissor hand block','平挟受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(123,'Nekozeken uchi age uke','Inside rising cat back fi','猫脊拳内揚げ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(124,'Hasami uke','Scissor block','鋏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(125,'Yoko ude hasami uke','Side forearm scissor bloc','横腕鋏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(126,'Tekubi nagashi uke','Flowing wrist block','手首流し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(127,'Soto haiwan uke','Outside back of arm block','中段外背腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(128,'Soto nagashi','Outside parry','中段外流し','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(129,'Soto ude uke','Outward forearm block','外腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(130,'Shutō uke','Sword hand block','手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(131,'Tate shutō uke','Vertical sword hand block','縦手刀受え','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(132,'Kake shutō uke','Hooking sword hand block','掛け手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(133,'Haishu uke','Back hand block','背手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(134,'Kakutō uke','Crane head block','鶴頭受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(135,'Kote uke','Circular upward block','小手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(136,'Hangetsu uke','Crescent moon block','半月受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(137,'Kaishu yoko uke','Open hand side block','開手中段横受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(138,'Yoko jūji uke','Side cross block','横十字受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(139,'Keitō uke','Chicken head block','鶏頭受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(140,'Morote uke','Augmented block','諸手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(141,'Haitō uke','Ridge hand block','背刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(142,'Sasae uke','Supported block','支え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(143,'Kakiwake uke','Reverse wedge block','掻き分け受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(144,'Morote yoko uke','Double side block','諸手横受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(145,'Yoko ude hasami uke','Side forearm scissors blo','横腕鋏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(146,'Kuri uke','Coiling elbow block','繰り受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(147,'Makite uke','Winding block','巻手受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(148,'Morote de wa uke','Two-handed circle block','諸手で輪受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(149,'Morote teishō harai uke','Augmented palm heel sweep','諸手底掌 払い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(150,'Ryūun no uke','Flowing cloud block','流雲の受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(151,'Seiryūtō awse uke','Combined ox-jaw hand bloc','青竜刀合せ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(152,'Tsuki uke','Punch block','突き受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(153,'Soto kake uke','Outside hooking block','外掛け受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(154,'Sokumen uke','Side block','側面受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(155,'Taihineri ura uke','Body twisting hooking blo','体捻り裏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(156,'Teishō hasami uke','Palm heel scissor block','底掌鋏受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(157,'Tekubi sokumen','手首側面掛受け','kake uke','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(158,'Ura gake uke','Backhand hooking block','裏掛け受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(159,'Morote kakete','Double hooking hands','中段諸手掛け手','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(160,'Soto mawashi uke','Sideways roundhouse block','外回し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(161,'Fumikomi ude uke','Stepping in forearm block','踏み込み腕受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(162,'Harai uke','Sweeping block','払い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(163,'Haitō morote uchi uke','Augmented inside ridgehan','背刀内 受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(164,'Gedan uke','Lower level blocks','下段受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(165,'Otoshi teishō uke','Dropping palm heel block','落とし底掌受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(166,'Otoshi seiryūtō uke','Dropping ox-jaw hand bloc','落とし青竜刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(167,'Ken jūji uke','Cross block with fists','拳十字受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(168,'Teishō awase uke','Combined palm heel block','底掌合せ受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(169,'Uchi otoshi uke','Inside dropping block','内落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(170,'Ken uke','Fist block','拳受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(171,'Morote seiken otoshi uke','Two-fisted combined dropp','諸手正拳落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(172,'Ryō shōtei osae uke','Two-handed palm heel pres','両掌底押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(173,'Seiken uke','Punch block','正拳受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(174,'Shōtei barai uke','Palm heel sweeping block','掌底払い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(175,'Taihineri barai uke','Body twisting down block','体捻り払い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(176,'Haishu otoshi uke','Back of hand dropping blo','右背手落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(177,'Harai osae uke','Sweeping pressing block','払い押え受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(178,'Hiji uke','Elbow block','肘受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(179,'Koken uke','Arc fist block','弧拳受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(180,'Suri otoshi uke','Dropping scraping block','擦リ落とし受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(181,'Gaiwan gedan uke','Downward outer forearm bl','外腕下段受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(182,'Uchi shutō uke','Inward sword hand block','內腕手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(183,'Uchi sukui uke','Inward scooping block','內掬い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(184,'Morote sukui uke','Two-handed scooping block','諸手掬い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(185,'Gedan barai','Downward sweep','下段払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(186,'Soto shutō uke','Outward sword hand block','外腕手刀受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(187,'Tekubi kake uke','Bent wrist block','手首掛受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(188,'Soto sukui uke','Outward','外掬い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(189,'Morote gedan barai','Lower level reverse wedge','諸手下段払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(190,'Sasae gedan barai','Supported lower sweep','支え下段払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(191,'Tsuki uke','Punch block','突き受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(192,'Gedan uke nagashi','Lower level flowing block','下段受け流し','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(193,'Harai sukui uke','Sweeping scooping block','払い掬い受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(194,'Morote shutō gedan barai','Lower-level double sword-','諸手手刀下段払い','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(195,'Jōge uke','High-low blocks','上下受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(196,'Kōsa uke','Cross block','交差受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(197,'Manji uke','Swastika block','卍受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(198,'Musō uke','Incomparable block','無双受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(199,'Hari uke','Archer block','張り受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(200,'Morote kokō uke','Double tiger mouth block','諸手虎口受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(201,'Ryō ude mawashi uke','Two-armed circular block','両腕回し受け','UKE',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(202,'Gyaku empi uchi','Reverse elbow strike','逆猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(203,'Oi empi uchi','Non-reverse elbow strike','追い猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(204,'Mae empi uchi','Front elbow strike','前猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(205,'Ushiro empi uchi','Backward elbow strike','後ろ猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(206,'Yoko empi uchi','Side elbow strike','横猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(207,'Tate empi uchi','Vertical elbow strike','縦猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(208,'Otoshi empi uchi','Dropping elbow strike','落とし猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(209,'Yoko mawashi empi uchi','Side roundhouse elbow str','横回し猿臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(210,'Soete mawashi empi uchi','Attached hand side elbow ','添え手回し臂打ち','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(211,'Kaiten hiji ate','Spinning elbow strike','回転肘当て','UCHI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(212,'Choku zuki','Straight punch','直突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(213,'Gyaku zuki','Reverse punch','逆突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(214,'Nobashi gyaku zuki','Extended reverse punch','伸ばし逆突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(215,'Oi zuki','Lunge  punch','追い突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(216,'Nobashi oi zuki','Extended lunge punch','伸ばし追い突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(217,'Age zuki','Rising punch','揚げ突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(218,'Ago zuki','Punch to the chin','顎突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(219,'Soko zuki','Bottom thrust','底突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(220,'Ura zuki','Inverted punch','裏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(221,'Tate zuki','Vertical punch','縦突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(222,'Yoko zuki','Side punch','横突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(223,'Yumi zuki','Bow punch','弓交き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(224,'Otoshi zuki','Dropping punch','落とし交き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(225,'Kizami zuki','Jab','刻み突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(226,'Kagi zuki','Hook punch','鉤突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(227,'Mawashi zuki','Roundhouse punch','回し突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(228,'Uchi oroshi zuki','Overhand punch','打ち下ろし突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(229,'Sasae zuki','Supported punch','支え突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(230,'Ryūsui zuki','Flowing water punch','流水突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(231,'Soete ura zuki','Attached hand inverted pu','添え手裏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(232,'Okuri zuki','Sliding punch','送リ突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(233,'Kusshin zuki','Drop dodge punch','屈伸突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(234,'Wari uke zuki','Circle block punch','割受け突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(235,'Hineri zuki','Twisting punch','捻り突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(236,'Ryūkyū zuki','¾ twisting punch','琉球突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(237,'Nagashi zuki','Flowing punch','流し突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(238,'Junzuki tsukkomi','Leaning lunge punch','順突き突っ込み','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(239,'Gyaku zuki tsukkomi','Leaning reverse punch','逆突き突っ込み','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(240,'Kōhō tsuki age','Uppercut to rear','後方突き揚げ','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(241,'Kawashi zuki','Evasion punch','躱し突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(242,'Shoken zuki','First knuckle punch','初拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(243,'Boshiken zuki','Thumb punch','拇指拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(244,'Kaku zuki','Square punch','角突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(245,'Kakushi zuki','Hidden fist punch','隠し突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(246,'Dakō zuki','Crawling punch','蛇行突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(247,'Mawashi gyaku zuki','Roundhouse reverse punch','回し逆突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(248,'Sokumen gyaku zuki','Roundhouse reverse punch','側面逆突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(249,'Sun  zuki','One inch punch','寸突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(250,'Shōtei zuki','Palm heel thrust','掌底突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(251,'Keikō ken zuki','Chicken beak fist punch','鶏口拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(252,'Ushiro zuki','Backward punch','後ろ突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(253,'Tobi zuki','Jumping punch','飛び突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(254,'Hiraken zuki','Flat fist punch','平拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(255,'Ura hiraken zuki','Inverted flat fist punch','裏平拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(256,'Shihon nukite','Four-finger spear-hand','四本贯手','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(257,'Nihon nukite','Two-finger spear-hand','二本貫手 T','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(258,'Ippon nukite','One-finger spear-hand','一本貫手','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(259,'Tate Nukite','Vertical sword-hand','縦貫手','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(260,'Ura nukite','Inverted spear-hand','裏貫手','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(261,'Awase zuki','Combined punch','合せ突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(262,'Yama zuki','Mountain punch','山突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(263,'Kasane zuki','Double punch','重ね突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(264,'Heikō zuki|','Parallel punch','並行突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(265,'Heikō tate zuki','Parallel standing fist th','並行縦手突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(266,'Morote hiraken zuki','Double flat fist punch','諸手平拳突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(267,'Jūji zuki','Cross thrust','十字突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(268,'Morote ura zuki','Double inverted punch','諸手裏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(269,'Morote kizami ura zuki','Double jabbing inverted p','諸手刻み裏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(270,'Ryō ippon ken choku zuki','Double one-knuckle punch','両一本拳直突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(271,'Hasami zuki','Scissor punch','鋏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(272,'Tate ken shita zuki','Downward punch with stand','縦拳下突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(273,'Kaiun no te','Parting the clouds','開雲の手','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(274,'Shutō jūji uchi','Sword hand cross strike','手刀十字打ち','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(275,'Morote shōtei zuki','Double palm heel thrust','諸手掌底突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(276,'Tora guchi','Tiger\'s mouth','虎口','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(277,'Morote nuki zuki','Double spear hand thrust','諸手貫突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(278,'Sayū zuki','Left-right thrust','左右突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(279,'Washide zuki age','Rising punch with eagle h','鷲手突き揚げ','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(280,'Ippon nukite chūdan otosh','Middle level one-finger s','一本貫手中段落とし突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(281,'Uwa uke zuki','Upward block punch','上受け突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(282,'Soto uke zuki','Outside block punch','外受け突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(283,'Morote shita zuki','Double low punch','両手裏突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(284,'Oshi zuki','Push thrust','押し突き','TSUKI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(285,'Mae geri','Front kick','前蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(286,'Mae kekomi','Front thrust kick','前蹴込','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(287,'Mae keage','Front rising kick','前蹴上げ','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(288,'Tobi mae geri','Flying front kick','飛び前蹴','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(289,'Mae taore geri','Falling front kick','前倒れ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(290,'Fumikomi','Stamping kick','踏み込み','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(291,'Uchi momo geri','Inside thigh kick','内股蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(292,'Yoko geri','Side kick','横蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(293,'Yoko kekomi','Side thrust kick','横蹴込','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(294,'Yoko keage','Side rising kick','横蹴上げ','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(295,'Tobi yoko geri','Flying side kick','飛び横蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(296,'Yoko taore geri','Falling side kick','横倒れ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(297,'Fumi kiri','Cutting kick','踏み切り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(298,'Kaiten yoko geri','Spinning side kick','回転横蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(299,'Mawashi geri','Roundhouse kick','回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(300,'Gyaku mawashi geri','Reverse roundhouse kick','逆回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(301,'Yoko mawashi geri','Side roundhouse kick','横回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(302,'Tobi mawashi geri','Jumping roundhouse kick','飛び回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(303,'Mawashi taore geri','Falling roundhouse kick','回し倒れ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(304,'Gedan mawashi geri','Low roundhouse kick','下段回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(305,'Kaiten mawashi geri','Spinning roundhouse kick','回転回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(306,'Ushiro geri','Back kick','後ろ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(307,'Kaiten ushiro geri','Spinning back kick','回転後ろ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(308,'Sempū tobi geri','Whirlwind kick','旋風飛び蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(309,'Tobi ushiro geri','Jumping back kick','飛び後ろ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(310,'Ebi geri','Shrimp kick','海老蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(311,'Sasori geri','Scorpion kick','蠍蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(312,'Dō mawashi kaiten geri','Rolling kick','胴廻し回転蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(313,'Ura mawashi geri','Hook kick','裏回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(314,'Ushiro mawashi geri','Spinning hook kick','後ろ回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(315,'Tobi ura mawashi geri','Jumping hook kick','飛び裏回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(316,'Tobi ushiro mawashi geri','Jumping spinning hook kic','飛び後ろ回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(317,'Kensei yuka geri','Diversion by kicking the ','牽制床蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(318,'Namigaeshi','Returning wave kick','波返し','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(319,'Mikazuki geri','Crescent kick','三日月蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(320,'Gyaku mikazuki geri','Reverse crescent kick','逆三日月蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(321,'Tsumasaki geri','Toe kick','爪先蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(322,'Kingeri','Groin kick','金蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(323,'Ushiro kingeri','Back groin kick','後ろ金蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(324,'Ushiro kake geri','Backward hooking kick','後ろ掛け蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(325,'Kaiten ushiro mawashi ger','Turning back roundhouse k','回転後ろ回し蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(326,'Nidan geri','Double kick','二段蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(327,'Mae sōsoku geri','Simultaneous kick to the ','前双足蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(328,'Sayū geri','Simultaneous kick to the ','左右蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(329,'Hasami geri','Scissor kick','鋏蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(330,'Ryō mae taore geri','Twin front falling kick','両前倒れ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(331,'Ryō ashi mawashi taore ge','Double falling roundhouse','両足回し倒れ蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(332,'Kakato otoshi geri','Axe kick','踵落とし蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(333,'Zageri','Seated kick','座蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(334,'Uchi haisoku geri','Inside kick with instep','內背足蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(335,'Mae sokutō geri','Front kick with foot swor','前足刀蹴り','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30'),(336,'Ōbāheddo kikku','Overhead kick','オーバーへッドキック','KERI',NULL,'2020-02-02 18:52:30','2020-02-02 18:52:30');
/*!40000 ALTER TABLE `glossary` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-07 20:44:59
