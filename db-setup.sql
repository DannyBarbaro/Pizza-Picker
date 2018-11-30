-- setup database and user
drop database if exists pizza;
create database pizza;
drop user if exists 'sommelier'@'localhost';
create user 'sommelier'@'localhost' identified by 'mamamia';
grant all on pizza.* to 'sommelier'@'localhost';
flush privileges;
use pizza;

-- create tables
CREATE TABLE User (
  username varchar(32) NOT NULL,
  password varchar(255) NOT NULL,
  PRIMARY KEY (username)
);

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('Conor','dontdoencryptionkids'),('Danny','notverysecure'),('Josh','securityisimportant');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Topping (
  name varchar(32) NOT NULL,
  PRIMARY KEY (name)
);

LOCK TABLES `Topping` WRITE;
/*!40000 ALTER TABLE `Topping` DISABLE KEYS */;
INSERT INTO `Topping` VALUES ('bacon'),('cheese'),('corn'),('ham'),('mushrooms'),('olives'),('onions'),('pepperoni'),('peppers'),('pineapple'),('sausage');
/*!40000 ALTER TABLE `Topping` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Allergy (
  user varchar(32) NOT NULL,
  topping varchar(32) NOT NULL,
  PRIMARY KEY (user, topping),
  FOREIGN KEY (user) REFERENCES User(username),
  FOREIGN KEY (topping) REFERENCES Topping(name)
);

LOCK TABLES `Allergy` WRITE;
/*!40000 ALTER TABLE `Allergy` DISABLE KEYS */;
INSERT INTO `Allergy` VALUES ('Danny','corn'),('Conor','ham'),('Conor','pineapple');
/*!40000 ALTER TABLE `Allergy` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Food_Order (
  order_id int(11) NOT NULL AUTO_INCREMENT,
  date datetime,
  PRIMARY KEY (order_id)
);

CREATE TABLE Order_Details (
  order_id int(11) NOT NULL,
  user varchar(32) NOT NULL,
  topping varchar(32) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Food_Order(order_id),
  FOREIGN KEY (user) REFERENCES User(username),
  FOREIGN KEY (topping) REFERENCES Topping(name)
);

CREATE TABLE Friends (
  friend1 varchar(32) NOT NULL,
  friend2 varchar(32) NOT NULL,
  PRIMARY KEY (friend1, friend2),
  FOREIGN KEY (friend1) REFERENCES User(username),
  FOREIGN KEY (friend2) REFERENCES User(username)
);

LOCK TABLES `Friends` WRITE;
/*!40000 ALTER TABLE `Friends` DISABLE KEYS */;
INSERT INTO `Friends` VALUES ('Danny','Conor'),('Josh','Conor'),('Conor','Danny'),('Josh','Danny'),('Conor','Josh'),('Danny','Josh');
/*!40000 ALTER TABLE `Friends` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Preference_Set (
  id int(11) NOT NULL AUTO_INCREMENT,
  user varchar(32) NOT NULL,
  title varchar(32) DEFAULT NULL,
  is_active tinyint(1) DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user) REFERENCES User(username)
);

LOCK TABLES `Preference_Set` WRITE;
/*!40000 ALTER TABLE `Preference_Set` DISABLE KEYS */;
INSERT INTO `Preference_Set` VALUES (1,'Josh','I like me my meats',1),(2,'Danny','Hawaiian Or Bust',0),(3,'Danny','Meat me in a Dark Alley',1),(4,'Conor','very accurate',1),(6,'Conor','I refuse to have an opinion',0);
/*!40000 ALTER TABLE `Preference_Set` ENABLE KEYS */;
UNLOCK TABLES;

CREATE TABLE Preference (
  topping varchar(32) NOT NULL,
  set_id int(11) NOT NULL,
  score int(11) NOT NULL,
  PRIMARY KEY (topping,set_id),
  FOREIGN KEY (set_id) REFERENCES Preference_Set(id)
);

LOCK TABLES `Preference` WRITE;
/*!40000 ALTER TABLE `Preference` DISABLE KEYS */;
INSERT INTO `Preference` VALUES ('bacon',1,1),('bacon',2,1),('bacon',3,1),('bacon',4,0),('bacon',6,0),('cheese',1,1),('cheese',2,1),('cheese',3,1),('cheese',4,-1),('cheese',6,0),('corn',1,-1),('corn',2,-1),('corn',4,1),('corn',6,0),('ham',1,1),('ham',2,1),('ham',3,1),('mushrooms',1,-1),('mushrooms',2,-1),('mushrooms',3,0),('mushrooms',4,0),('mushrooms',6,0),('olives',1,-1),('olives',2,-1),('olives',3,0),('olives',4,0),('olives',6,0),('onions',1,-1),('onions',2,-1),('onions',3,0),('onions',4,0),('onions',6,0),('pepperoni',1,1),('pepperoni',2,-1),('pepperoni',3,1),('pepperoni',4,0),('pepperoni',6,0),('peppers',1,-1),('peppers',2,-1),('peppers',3,0),('peppers',4,0),('peppers',6,0),('pineapple',1,-1),('pineapple',2,1),('pineapple',3,-1),('sausage',1,1),('sausage',2,-1),('sausage',3,1),('sausage',4,0),('sausage',6,0);
/*!40000 ALTER TABLE `Preference` ENABLE KEYS */;
UNLOCK TABLES;