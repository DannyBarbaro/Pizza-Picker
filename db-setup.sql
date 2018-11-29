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

CREATE TABLE Topping (
  name varchar(32) NOT NULL,
  PRIMARY KEY (name)
);

CREATE TABLE Allergy (
  user varchar(32) NOT NULL,
  topping varchar(32) NOT NULL,
  PRIMARY KEY (user, topping),
  FOREIGN KEY (user) REFERENCES User(username),
  FOREIGN KEY (topping) REFERENCES Topping(name)
);

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

CREATE TABLE Preference_Set (
  id int(11) NOT NULL AUTO_INCREMENT,
  user varchar(32) NOT NULL,
  title varchar(32) DEFAULT NULL,
  is_active tinyint(1) DEFAULT NULL,
  is_dislike tinyint(1) DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user) REFERENCES User(username)
);

CREATE TABLE Preference (
  topping varchar(32) NOT NULL,
  set_id int(11) NOT NULL,
  score int(11) NOT NULL,
  PRIMARY KEY (topping,set_id),
  FOREIGN KEY (set_id) REFERENCES Preference_Set(id)
);