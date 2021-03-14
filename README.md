# Avaliação técnica Coffebean

## Requirements:

- Python 3
- MySQL Community Server and MySQL Workbench
- Python Flask (install with "pip install flask")
- Flask-MySQLdb (install with "pip install flask-mysqldb")

## Creating the database:

- In MySQL Workbench, copy the following code and execute:

  CREATE DATABASE IF NOT EXISTS `coffebean` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
  USE `coffebean`;

  CREATE TABLE IF NOT EXISTS `accounts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(50) NOT NULL,
      `password` varchar(255) NOT NULL,
      `email` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');

## How to execute:

- Run MySQL server
- At the destination folder (...\coffebean), run the following commands on your Command Prompt:
  - set FLASK_APP=main.py
  - flask run
 
 In your browser, open the following link:
 
 -http://localhost:5000/coffebean/
 
 The following username, password and email are already registered and used for testing the application:
 - Username: test
 - Password: test
 - Email: test@test.com
