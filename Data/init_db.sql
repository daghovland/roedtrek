DROP TABLE IF EXISTS users;
CREATE TABE users (
       id INT NOT NULL AUTO_INCREMENT,
       name VARCHAR(255) NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL,
       PRIMARY KEY(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS roles;
CREATE TABE users (
       id INT NOT NULL AUTO_INCREMENT,
       name VARCHAR(255) NOT NULL,
       PRIMARY KEY(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS groups;
CREATE TABLE local_groups (
       id INT NOT NULL AUTO_INCREMENT, 
       name VARCHAR(255) NOT NULL,
       PRIMARY KEY(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS user_roles;
CREATE TABLE user_roles (
       id INT NOT NULL AUTO_INCREMENT,
       user_id INT NOT NULL, 
       role_id INT NOT NULL,
       PRIMARY KEY(id),
       FOREIGN KEY (role_id) REFERENCES roles(id),
       FOREIGN KEY (user_id) REFERENCES users(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
       `id` INT NOT NULL AUTO_INCREMENT, 
       code VARCHAR(10) NOT NULL, 
       name VARCHAR(200) NOT NULL,
       parent INT,
       group_id INT NOT NULL,
       PRIMARY KEY (id),
       FOREIGN KEY (parent) REFERENCES accounts(id),
       FOREIGN KEY (group_id) REFERENCES groups(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
       `id` INT NOT NULL AUTO_INCREMENT,
       `from` INT  NOT NULL,
       `to` INT NOT NULL,
       PRIMARY KEY (`id`),
       FOREIGN KEY (`from`) REFERENCES accounts(id),
       FOREIGN KEY (`to`) REFERENCES accounts(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
       id INT NOT NULL AUTO_INCREMENT,
       group_id INT NOT NULL,	
       name VARCHAR(255) NOT NULL,
       PRIMARY KEY(id))
ENGINE=InnoDB DEFAULT CHARSET=utf8;
