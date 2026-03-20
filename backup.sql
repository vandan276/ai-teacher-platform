-- MySQL dump 10.13  Distrib 9.6.0, for macos26.2 (arm64)
--
-- Host: localhost    Database: teacher_platform
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'cbcdd97a-21df-11f1-b5eb-43dd8c2411e6:1-156';

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `priority` enum('normal','important','urgent') DEFAULT 'normal',
  `created_by` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'hello users','hello users','normal',1,'2026-03-18 14:30:11');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessments`
--

DROP TABLE IF EXISTS `assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `question` text NOT NULL,
  `option_a` text NOT NULL,
  `option_b` text NOT NULL,
  `option_c` text NOT NULL,
  `option_d` text NOT NULL,
  `correct_answer` enum('A','B','C','D') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `assessments_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessments`
--

LOCK TABLES `assessments` WRITE;
/*!40000 ALTER TABLE `assessments` DISABLE KEYS */;
INSERT INTO `assessments` VALUES (3,2,'AI has the potential to support educators by:','Creating engaging slides for a lesson with Power Point Designer','Conferencing with learners and building relationships','Creating more work for the educator to complete','None of the above','A'),(4,2,'What does a generative AI model do differently compared to AI we’ve already been using?','Analyzes data to predict future outcomes','Recognizes patterns in data and uses these patterns to generate new content','Recognizes patterns in data and creates factual information each time','It doesn’t handle data','B'),(5,2,'What’s one of the most important details to remember when using a generative AI program?','Speed','Popularity','Accuracy','The cost','C'),(6,3,'Which AI tool can help educators work efficiently by generating content like text, images, and code?','Khanmigo','Microsoft Copilot','Learning Accelerators','PowerPoint Designer','B'),(7,3,'How can GitHub Copilot assist educators and learners in coding?','By suggesting code completion and corrections','By providing real-time coaching and feedback','By managing class resources and lesson plans','By replacing the need for coding knowledge','A'),(8,3,'What is one of the benefits of using Learning Accelerators in education?','To reduce the need for professional development','To replace traditional teaching methods','To support learners with real-time coaching','To eliminate the need for assessment','C'),(9,4,'Which tasks can Microsoft Copilot Chat perform to assist teaching and learning?','Search results from the web, summarize information, and provide links to sources','Determine which teaching methods are best for learners in a class','Guarantee accuracy of all search results','Automatically grade all essay assignments','A'),(10,4,'What’s the primary purpose of using prompts in Copilot Chat?','To provide specific instructions or context to generate relevant responses','To test its ability to understand random words','To limit responses to a predefined set of answers','To bypass security filters','A'),(11,4,'What is \"Iterative Prompting\"?','Repeating the same prompt multiple times','Continuing the conversation to refine response results','Using multiple languages in one prompt','Generating images instead of text','B'),(12,5,'Which specific elements does effective prompting include?','Persona, quotes, audience, reasons, and question','Goal, context, expectations, source','Effective prompting doesn\'t require any specific elements','Random keywords and symbols','B'),(13,5,'How are searching and prompting different?','Searching finds existing content via keywords; Prompting generates responses with citations from data','Searching and prompting are the same','Searching creates original responses; Prompting asks for a single source','Prompting is only for images, searching is only for text','A'),(14,5,'What tools can learners use to create engaging presentations?','Minecraft Education, Stream, and Edge','Microsoft Designer, Clipchamp, and PowerPoint Designer','Word, Excel, and OneNote','None of the above','B');
/*!40000 ALTER TABLE `assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `districts`
--

DROP TABLE IF EXISTS `districts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `districts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `district_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `district_name` (`district_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `districts`
--

LOCK TABLES `districts` WRITE;
/*!40000 ALTER TABLE `districts` DISABLE KEYS */;
INSERT INTO `districts` VALUES (1,'Ahmedabad'),(5,'Bhavnagar'),(7,'Gandhinagar'),(6,'Jamnagar'),(4,'Rajkot'),(2,'Surat'),(3,'Vadodara');
/*!40000 ALTER TABLE `districts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `event_type` enum('meeting','training','event','deadline') DEFAULT 'event',
  `event_date` date NOT NULL,
  `event_time` time DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `created_by` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (3,'meeting','meeting','meeting','2026-03-18',NULL,'online',1,'2026-03-18 16:26:16','https://meet.google.com/why-wnqr-nmn');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `is_read` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,1,3,'hhiii]','2026-03-18 12:42:02',0),(2,1,3,'Hello from Admin! How is the monitoring going?','2026-03-18 12:42:54',0),(3,1,11,'hello','2026-03-18 12:43:59',1),(4,1,9,'hii','2026-03-18 14:17:34',1),(5,9,1,'hi','2026-03-18 14:19:00',1),(6,9,1,'hi','2026-03-18 14:19:19',1),(7,9,13,'hi','2026-03-18 14:20:17',0),(8,19,1,'hi','2026-03-18 16:45:28',1),(9,19,1,'hi','2026-03-18 16:45:51',1),(10,19,1,'hi','2026-03-18 16:45:57',1),(11,1,19,'hii','2026-03-18 16:46:26',1),(12,1,19,'hii','2026-03-18 16:46:39',1),(13,19,1,'who are you','2026-03-18 16:46:42',0),(14,1,9,'hii','2026-03-19 15:27:38',0);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modules`
--

DROP TABLE IF EXISTS `modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `content` text,
  `category` varchar(100) DEFAULT 'General AI',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modules`
--

LOCK TABLES `modules` WRITE;
/*!40000 ALTER TABLE `modules` DISABLE KEYS */;
INSERT INTO `modules` VALUES (2,'Empower educators to explore the potential of AI','Learn to use AI, generative AI, and Microsoft tools to personalize learning, automate tasks, and provide insights for education.','# Empower educators to explore the potential of artificial intelligence\n\n## Learning Objectives\n- Describe generative AI in the broader context of AI.\n- Explain what a large language model (LLM) is and how it works.\n- Use generative and summative capabilities of LLMs.\n- Explain how AI improves learning outcomes and reduces educator workload.\n- Explore AI for accessibility and inclusion.\n\n## Core Content\n### Introduction to AI\nArtificial Intelligence (AI) is the ability of a computer system to perform tasks that would normally require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.\n\n### Generative AI\nGenerative AI is a type of AI that can create new content, such as text, images, or audio, based on the data it has been trained on. It uses patterns and structures learned from existing data to generate original output.\n\n### Large Language Models (LLMs)\nLarge Language Models are AI systems trained on massive amounts of text data. They can understand and generate human-like text, answer questions, summarize documents, and even write code.\n\n### AI in Education\nAI can personalize learning by adapting to each student\'s needs, automate administrative tasks for teachers, and provide real-time feedback to learners.','General AI'),(3,'Embark on Your AI Journey with Free AI Tools from Microsoft Education','Intro to powerful AI tools from Microsoft Education for streamlined workflows and enhanced feedback.','# Embark on Your AI Journey with Free AI Tools from Microsoft Education\n\n## Learning Objectives\n- Use AI tools to streamline workflows and focus on teaching.\n- Provide detailed feedback and personalized learning experiences.\n- Create engaging lesson plans and interactive lessons with AI.\n- Use AI to improve coding and future-ready skills.\n\n## Core Content\n### Bring Opportunity to Schools with AI\nAI tools can help schools provide equitable access to quality education. They can support diverse learning needs and help educators manage large classrooms more effectively.\n\n### Work Efficiently with Microsoft 365 Copilot Chat\nCopilot Chat allows educators to draft emails, create lesson plans, and summarize long documents quickly, saving valuable time for direct student interaction.\n\n### Learning Accelerators\nMicrosoft Learning Accelerators like Reading Progress and Search Progress use AI to help students build foundational skills and improve literacy.\n\n### Save Time with Microsoft Teams\nIntegration of AI in Teams for Education helps automate grading, organize assignments, and track student progress seamlessly.','General AI'),(4,'Enhance Teaching and Learning with Microsoft 365 Copilot Chat','Strategies for leveraging Copilot Chat including prompt design tips and responsible AI practices.','# Enhance Teaching and Learning with Microsoft 365 Copilot Chat\n\n## Learning Objectives\n- Summarize basic uses of Copilot Chat for educators.\n- Design effective prompts to support teaching and learning.\n- Evaluate AI-generated responses for quality and credibility.\n- Implement responsible AI practices in the classroom.\n\n## Core Content\n### Explore Copilot Chat\nCopilot Chat is a conversational AI assistant that can help with a wide range of tasks from brainstorming creative ideas to answering complex questions.\n\n### Design Prompts for Learning\nThe \"prompt\" is the instruction you give to the AI. Effective prompts are specific, provide context, and define the desired output format.\n\n### Evaluate Responses\nWhile AI is powerful, it can sometimes produce inaccurate information (hallucinations). Educators must critically assess AI outputs for accuracy and bias.\n\n### Working with Images\nAI-powered image generation can help teachers create visual aids, diagrams, and illustrative examples for their students.','General AI'),(5,'Equip and Support Learners with AI Tools from Microsoft','Help learners interact with AI tools like Copilot, including responsible use and prompt engineering.','# Equip and Support Learners with AI Tools from Microsoft\n\n## Learning Objectives\n- Teach learners to thoughtfully engage with AI.\n- Explain how learners can be responsible users of AI.\n- Support learners in learning prompt engineering.\n- Explore AI\'s potential for learners to become changemakers.\n\n## Core Content\n### Critical Thinking in the Age of AI\nStudents need to develop \"AI Literacy\" — understanding how AI works and being able to question the information it provides.\n\n### Learners as Responsible Users\nResponsible AI use includes respecting copyright, protecting privacy, and understanding the environmental impact of AI systems.\n\n### Prompt Engineering for Students\nTeaching students how to phrase their queries effectively helps them get better results and understand the logic behind AI reasoning.\n\n### Learners as Changemakers\nAI can be a powerful tool for students to solve real-world problems in their communities, from environmental monitoring to accessibility improvements.','General AI');
/*!40000 ALTER TABLE `modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `module_id` int NOT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_module` (`user_id`,`module_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `progress_ibfk_2` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

LOCK TABLES `progress` WRITE;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
INSERT INTO `progress` VALUES (2,7,2,1),(3,7,3,1),(4,7,4,1),(5,7,5,1);
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `file_url` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT 'General',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources`
--

LOCK TABLES `resources` WRITE;
/*!40000 ALTER TABLE `resources` DISABLE KEYS */;
INSERT INTO `resources` VALUES (2,'Prompt Engineering for Educators','Advanced techniques for better classroom prompts.','/static/docs/prompt_guide.pdf','Technical'),(3,'Copilot and PowerPoint Guide','Learn how to use Copilot to create stunning presentations.','/static/documents/Copilot and Powerpoint.pptx','Microsoft 365'),(4,'Training Day 1 Material','Core training materials for the first day of the program.','/static/documents/Day 1.pptx','Training'),(5,'Gujarati: Copilot and Word','Guide for using Copilot in Microsoft Word (Gujarati).','/static/documents/Guj Co PIlot and Word.pptx','Gujarati'),(6,'Gujarati: Training Day 1','Training materials for Day 1 translated in Gujarati.','/static/documents/Guj Day 1 (1).pptx','Gujarati'),(7,'Immersive Reader Guide','Master the use of Immersive Reader for inclusive classrooms.','/static/documents/Immersive Reader.pdf','Tools'),(8,'LLMs for Teachers','A comprehensive guide on Large Language Models for educators.','/static/documents/LLMs_for_Teachers.pptx','General AI'),(10,'Microsoft Elevate Training (Gujarati)','Full training deck for Microsoft Elevate in Gujarati.','/static/documents/Microsoft_Elevate_AI_Training_Gujarati.pptx','Gujarati');
/*!40000 ALTER TABLE `resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `module_id` int NOT NULL,
  `score` int NOT NULL,
  `passed` tinyint(1) DEFAULT '0',
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES (8,7,2,3,1,'2026-03-17 22:53:50'),(9,7,3,2,0,'2026-03-17 22:54:28'),(10,7,3,1,0,'2026-03-17 22:54:38'),(11,7,3,1,0,'2026-03-17 22:55:01'),(12,7,3,2,0,'2026-03-17 22:55:26'),(13,7,3,1,0,'2026-03-17 22:55:40'),(14,7,3,2,0,'2026-03-17 22:56:05'),(15,7,3,1,0,'2026-03-17 22:56:16'),(16,7,3,3,1,'2026-03-17 22:56:54'),(17,7,4,3,1,'2026-03-17 22:57:34'),(18,7,5,3,1,'2026-03-17 22:58:17');
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trophies`
--

DROP TABLE IF EXISTS `trophies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trophies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `achieved` tinyint(1) DEFAULT '0',
  `achieved_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_trophy` (`user_id`),
  CONSTRAINT `trophies_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trophies`
--

LOCK TABLES `trophies` WRITE;
/*!40000 ALTER TABLE `trophies` DISABLE KEYS */;
INSERT INTO `trophies` VALUES (1,7,1,'2026-03-17 22:58:17');
/*!40000 ALTER TABLE `trophies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('Admin','Employee','Participant') NOT NULL,
  `district_id` int DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `district_id` (`district_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Super Admin','admin@platform.com','pbkdf2:sha256:260000$Jdite173CH60VoLf$513f0aa85452f0907cf12b0f9a3f6c595c3fb81c538f3d087911f9f1ebdad7a6','Admin',NULL,1),(3,'vandan2','employee@platform.com','pbkdf2:sha256:260000$Egw4iwprouSfwOLS$fd0d64b03ea3945b6194a1f12dc9830404848f42e5a3250c022481023d22332f','Employee',3,1),(6,'xyz','employee3@platform.com','pbkdf2:sha256:260000$JrJr6nskxjS8r5EW$f7e4e6ce1516fc3c8af2be2e2f09fdd09c684b5bac51cb5dcebc5eb9e528d135','Participant',1,1),(7,'xyz','xyz@xyz.com','pbkdf2:sha256:260000$t4lDbcVGxFdQbqMj$e8fbdcd71dcb3bcf6be47c8e0962ce23820f6aa3149aafcea9019eb64e63bf85','Participant',1,1),(8,'Test employee','employee2@platform.com','pbkdf2:sha256:260000$gOTrekCl8KHUCVIr$48e60c4c28f62860ecdfbd2eb61107ea0555975cf3dacd0e6a1f19dba1f7d79a','Employee',1,1),(9,'Itisha Danger','itisha2001@gmail.com','scrypt:32768:8:1$elsWzFMwZo6wsJvw$52baca52a23f40730f9184ce1d2a0dbb220fd8ab825e3663beff8b8a845e6ccaed57be3a4ea9df392a320fe12a392a38992e8f9a0cb0e276c2ce5930d53f68bd','Employee',NULL,1),(10,'vandan4','xyz4@xyz.com','scrypt:32768:8:1$iJZxVKhhxSqlt4J9$0437c54d5cb825c4b75ed20e2ba42643db7cb0971d349a95fa79701b885aec94cfc1b4b15d98a516c59e0685a93b7ccb96db238c57bdc01fadfcdcfa79c0b269','Participant',7,1),(11,'xyzz','xyzz@platform.com','scrypt:32768:8:1$V1m2aDMXkwdmV3sg$55e8f09208fc2b65f4bdb93d6698fceae187c38f94607da31773beb1507900590e343ade5c56b6faf534c21566522c316752f1a433be958d849382558a1b9214','Employee',2,1),(12,'vandan','vandan4@xyz.com','scrypt:32768:8:1$x1BekxHs7zqRNUVv$b4eabf2cd37896c68da87a60f3870078a83c0c63925a16ad32a7620769c0b1e481ecfd1753273e043c7642fcab41fcd977b5607b9e5dd950adc314c8e0552056','Participant',5,1),(13,'adarsh','2xyz@xyz.com','scrypt:32768:8:1$Zc2dOMb8H9y3yfWY$a1a5336386f56c59f9b7236fcfbd9000eaf2fff4f13fda50f5d30da3538cdc84983c0f1708f75f836dca1fb5375f106b896a38879dad2b733b9962476ff8ccc6','Employee',NULL,1),(14,'G CM n','abc@gmail.com','scrypt:32768:8:1$E2KzJaeBmK0Qh7qZ$ce3327732226ddefd206940a6980b58070227161075e5f62f4320b530674f1f66a4ab8c2f93d0719ebeee86dc694ca803dfae5eb865b9a45b8a8e16db07b3910','Participant',3,1),(18,'John Cena ','john@test.com','scrypt:32768:8:1$poloRxHv4CpQRJUo$d15be0f53055bff1cfa90904f7f39d09efd8239050ca7055435a06b455f4d2f43dd8254f05707a96ba6dfa5e147f72af6dfbd4fcb3ec5e0a900d3b671722f844','Participant',3,1),(19,'new ','new@platform.com','scrypt:32768:8:1$bsPdhLsgxEYIUYvu$d88d92ee9ce701e7f2887a1b91026d1d22d51ef583706185d4e9000db736a4da682cc490c9582a5984889f80df3017869486aaa32ab602fad40f483b15be02f8','Employee',NULL,1),(20,'Vandan Panchal','panchalvandan8@gmail.com','OAUTH_USER','Participant',NULL,1),(21,'Adarsh Biju','abx246457@gmail.com','OAUTH_USER','Participant',NULL,1),(22,'Kolechery Adarsh Biju','kolenchery246457@gmail.com','OAUTH_USER','Participant',NULL,1),(23,'VANDAN Panchal','heenapanchal2811@gmail.com','OAUTH_USER','Participant',NULL,1),(24,'demo','demo@xyz.com','scrypt:32768:8:1$0rWdRf1IMSTPLzAD$84ccbca64adef0d6e34f0ff4722f9035ad194abab2a5fd0f87149a91268b14e74558d9c94653396f7610fb5cf51434e5ee8b7cbb8fddf4bc820443800284b242','Participant',3,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-20 10:18:47
