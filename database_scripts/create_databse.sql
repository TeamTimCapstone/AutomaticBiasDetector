CREATE DATABASE Bias_Detector;
USE Bias_Detector;

-- Websites that have articles/pages
CREATE TABLE Website
(
    website_url varchar(750),
    bias_rating decimal(16, 15) DEFAULT 0.0,
    article_count int DEFAULT 0,
    PRIMARY KEY (website_url)
);

-- Specific web articles/pages
CREATE TABLE Article
(
    article_url varchar(750),
    bias_rating decimal(16, 15) DEFAULT 0.0,
    website_url varchar(750),
    PRIMARY KEY (article_url),
    FOREIGN KEY (website_url) REFERENCES Website(website_url)
);

-- Specific sentences in an article that are flagged as biased
CREATE TABLE Bias_Instances
(
    id int AUTO_INCREMENT,
    article_url varchar(750) NOT NULL,
    sentence varchar(750) NOT NULL,
    bias_rating decimal(16, 15) DEFAULT 0.0,
    PRIMARY KEY (id),
    FOREIGN KEY (article_url) REFERENCES Article(article_url)
);

-- Words in a bias instance that are specifically biased
CREATE TABLE Biased_Words
(
    instance_id int NOT NULL,
    word varchar(256),
    FOREIGN KEY (instance_id) REFERENCES Bias_Instances(id)
);

-- A list of groups that are checked for bias against
CREATE TABLE Biased_Groups
(
    biased_group varchar(128),
    PRIMARY KEY (biased_group)
);

-- Groups that are the targets of bias in a specific instance
CREATE TABLE Bias_Instance_Groups
(
    instance_id int NOT NULL,
    biased_group varchar(128) NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES Bias_Instances(id),
    FOREIGN KEY (biased_group) REFERENCES Biased_Groups(biased_group)
);

-- Users
CREATE TABLE Users
(
    email varchar(256),
    password varchar(128) NOT NULL,
    PRIMARY KEY (email)
);
