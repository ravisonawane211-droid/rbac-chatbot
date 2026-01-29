INSERT INTO locations(location_id,country,city,cost_index) VALUES (1,'United States','San Francisco',1.35);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (2,'United States','New York',1.3);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (3,'United States','Austin',1.05);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (4,'Canada','Toronto',1.1);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (5,'United Kingdom','London',1.25);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (6,'Germany','Berlin',1.1);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (7,'France','Paris',1.18);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (8,'Spain','Barcelona',1.05);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (9,'Netherlands','Amsterdam',1.15);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (10,'Poland','Warsaw',0.95);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (11,'India','Bengaluru',0.7);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (12,'India','Hyderabad',0.68);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (13,'Egypt','Cairo',0.55);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (14,'UAE','Dubai',1.05);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (15,'South Africa','Cape Town',0.7);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (16,'Brazil','São Paulo',0.8);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (17,'Mexico','Mexico City',0.78);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (18,'Argentina','Buenos Aires',0.65);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (19,'Japan','Tokyo',1.2);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (20,'Singapore','Singapore',1.22);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (21,'Australia','Sydney',1.15);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (22,'India','Ahmedabad',0.7);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (23,'India','Pune',0.5);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (24,'India','Lucknow',0.6);
INSERT INTO locations(location_id,country,city,cost_index) VALUES (25,'India','Delhi',0.6);
INSERT INTO departments(department_id,department_name) VALUES (1,'Sales');
INSERT INTO departments(department_id,department_name) VALUES (2,'Finance');
INSERT INTO departments(department_id,department_name) VALUES (3,'Business');
INSERT INTO departments(department_id,department_name) VALUES (4,'Marketing');
INSERT INTO departments(department_id,department_name) VALUES (5,'Quality Assurance');
INSERT INTO departments(department_id,department_name) VALUES (6,'Operations');
INSERT INTO departments(department_id,department_name) VALUES (7,'HR');
INSERT INTO departments(department_id,department_name) VALUES (8,'Technology');
INSERT INTO departments(department_id,department_name) VALUES (9,'Compliance');
INSERT INTO departments(department_id,department_name) VALUES (10,'Data');
INSERT INTO departments(department_id,department_name) VALUES (11,'Risk');
INSERT INTO departments(department_id,department_name) VALUES (12,'Product');
INSERT INTO departments(department_id,department_name) VALUES (13,'Design');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1000','Aadhya Patel','aadhya.patel@fintechco.com','Sales Manager',1,22,'FINEMP1006','2018-11-20');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1001','Isha Chowdhury','isha.chowdhury@fintechco.com','Credit Officer',2,23,'FINEMP1005','2021-05-20');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1002','Sakshi Malhotra','sakshi.malhotra@fintechco.com','Relationship Manager',1,22,'FINEMP1008','2023-04-17');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1003','Krishna Malhotra','krishna.malhotra@fintechco.com','Business Analyst',3,23,'FINEMP1003','2018-06-10');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1004','Aadhya Saxena','aadhya.saxena@fintechco.com','Marketing Manager',4,24,'FINEMP1008','2022-12-20');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1005','Shaurya Joshi','shaurya.joshi@fintechco.com','Financial Analyst',2,25,'FINEMP1009','2020-10-31');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1006','Sara Sharma','sara.sharma@fintechco.com','QA Engineer',5,25,'FINEMP1004','2021-05-15');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1007','Prisha Mehta','prisha.mehta@fintechco.com','Marketing Manager',4,11,'FINEMP1000','2020-11-30');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1008','Aadhya Chowdhury','aadhya.chowdhury@fintechco.com','Customer Support',6,1,'FINEMP1007','2019-02-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1009','Sai Gupta','sai.gupta@fintechco.com','Credit Officer',2,11,'FINEMP1009','2021-10-13');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1010','Vihaan Chowdhury','vihaan.chowdhury@fintechco.com','HR Manager',7,24,'FINEMP1007','2021-10-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1011','Sai Sharma','sai.sharma@fintechco.com','Business Analyst',3,22,'FINEMP1004','2021-05-21');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1012','Ishaan Patel','ishaan.patel@fintechco.com','Security Engineer',8,11,'FINEMP1007','2021-03-14');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1013','Prisha Banerjee','prisha.banerjee@fintechco.com','Security Engineer',8,11,'FINEMP1009','2020-04-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1014','Isha Desai','isha.desai@fintechco.com','Treasury Analyst',2,11,'FINEMP1002','2023-03-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1015','Ananya Singh','ananya.singh@fintechco.com','HR Manager',7,22,'FINEMP1001','2018-08-17');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1016','Ananya Reddy','ananya.reddy@fintechco.com','Relationship Manager',1,22,'FINEMP1003','2020-07-10');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1017','Prisha Saxena','prisha.saxena@fintechco.com','DevOps Engineer',8,11,'FINEMP1004','2019-10-20');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1018','Vivaan Reddy','vivaan.reddy@fintechco.com','Compliance Officer',9,11,'FINEMP1001','2024-11-17');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1019','Isha Chowdhury','isha.chowdhury1@fintechco.com','Relationship Manager',1,24,'FINEMP1000','2019-03-06');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1020','Krishna Verma','krishna.verma@fintechco.com','Sales Manager',1,1,'FINEMP1007','2024-11-29');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1021','Vihaan Verma','vihaan.verma@fintechco.com','Treasury Analyst',2,25,'FINEMP1006','2022-05-29');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1022','Sai Khan','sai.khan@fintechco.com','Customer Support',6,24,'FINEMP1005','2023-09-07');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1023','Krishna Gupta','krishna.gupta@fintechco.com','Business Analyst',3,24,'FINEMP1004','2024-05-06');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1024','Reyansh Mehta','reyansh.mehta@fintechco.com','Security Engineer',8,25,'FINEMP1001','2023-03-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1025','Krishna Reddy','krishna.reddy@fintechco.com','Marketing Manager',4,11,'FINEMP1004','2021-06-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1026','Ishaan Patel','ishaan.patel@fintechco.com','Blockchain Developer',8,25,'FINEMP1007','2024-08-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1027','Myra Desai','myra.desai@fintechco.com','Security Engineer',8,22,'FINEMP1009','2019-02-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1028','Isha Nair','isha.nair@fintechco.com','Compliance Officer',9,11,'FINEMP1007','2024-06-04');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1029','Aditya Patel','aditya.patel@fintechco.com','Data Analyst',10,23,'FINEMP1009','2020-01-17');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1030','Vihaan Reddy','vihaan.reddy@fintechco.com','Data Scientist',10,11,'FINEMP1003','2020-04-27');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1031','Isha Desai','isha.desai@fintechco.com','Compliance Officer',9,24,'FINEMP1009','2023-12-16');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1032','Arjun Desai','arjun.desai@fintechco.com','Financial Analyst',2,22,'FINEMP1009','2024-10-21');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1033','Saanvi Bhat','saanvi.bhat@fintechco.com','Risk Analyst',11,11,'FINEMP1003','2022-06-26');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1034','Diya Desai','diya.desai@fintechco.com','Marketing Manager',4,22,'FINEMP1002','2023-01-09');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1035','Arjun Chopra','arjun.chopra@fintechco.com','Treasury Analyst',2,11,'FINEMP1005','2019-02-20');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1036','Avni Khan','avni.khan@fintechco.com','Business Analyst',3,11,'FINEMP1002','2022-05-08');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1037','Vihaan Garg','vihaan.garg@fintechco.com','Sales Manager',1,12,'FINEMP1001','2023-02-05');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1038','Diya Bhat','diya.bhat@fintechco.com','Security Engineer',8,23,'FINEMP1007','2018-02-22');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1039','Sai Desai','sai.desai@fintechco.com','DevOps Engineer',8,11,'FINEMP1005','2021-08-28');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1040','Vihaan Reddy','vihaan.reddy@fintechco.com','QA Engineer',5,11,'FINEMP1006','2021-04-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1041','Shaurya Joshi','shaurya.joshi@fintechco.com','Relationship Manager',1,1,'FINEMP1000','2023-06-15');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1042','Vihaan Desai','vihaan.desai@fintechco.com','Customer Support',6,23,'FINEMP1007','2024-03-28');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1043','Aadhya Singh','aadhya.singh@fintechco.com','Sales Manager',1,23,'FINEMP1000','2024-06-02');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1044','Isha Desai','isha.desai@fintechco.com','Software Engineer',8,11,'FINEMP1008','2021-12-03');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1045','Ananya Banerjee','ananya.banerjee@fintechco.com','Data Analyst',10,1,'FINEMP1000','2023-10-29');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1046','Shaurya Joshi','shaurya.joshi@fintechco.com','Marketing Manager',4,24,'FINEMP1008','2018-11-03');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1047','Ishaan Singh','ishaan.singh@fintechco.com','Business Analyst',3,11,'FINEMP1007','2018-11-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1048','Isha Singh','isha.singh@fintechco.com','Financial Analyst',2,25,'FINEMP1008','2023-03-26');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1049','Arjun Garg','arjun.garg@fintechco.com','Product Manager',12,11,'FINEMP1005','2024-05-08');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1050','Myra Gupta','myra.gupta@fintechco.com','QA Engineer',5,24,'FINEMP1008','2021-02-01');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1051','Reyansh Saxena','reyansh.saxena@fintechco.com','Security Engineer',8,11,'FINEMP1000','2023-09-01');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1052','Ishaan Singh','ishaan.singh@fintechco.com','Relationship Manager',1,24,'FINEMP1000','2018-07-09');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1053','Isha Sharma','isha.sharma@fintechco.com','Customer Support',6,24,'FINEMP1002','2020-11-08');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1054','Ishaan Singh','ishaan.singh@fintechco.com','Data Scientist',10,25,'FINEMP1004','2019-10-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1055','Aditya Saxena','aditya.saxena@fintechco.com','HR Manager',7,22,'FINEMP1009','2024-09-30');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1056','Saanvi Bhat','saanvi.bhat@fintechco.com','UX Designer',13,25,'FINEMP1004','2018-08-15');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1057','Aditya Kapoor','aditya.kapoor@fintechco.com','Marketing Manager',4,24,'FINEMP1006','2022-04-22');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1058','Avni Chopra','avni.chopra@fintechco.com','Financial Analyst',2,11,'FINEMP1006','2019-09-03');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1059','Saanvi Malhotra','saanvi.malhotra@fintechco.com','Customer Support',6,24,'FINEMP1006','2018-08-30');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1060','Arjun Mehta','arjun.mehta@fintechco.com','Sales Manager',1,11,'FINEMP1007','2020-11-05');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1061','Vivaan Chowdhury','vivaan.chowdhury@fintechco.com','Blockchain Developer',8,12,'FINEMP1008','2020-03-01');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1062','Ananya Iyer','ananya.iyer@fintechco.com','Product Manager',12,11,'FINEMP1007','2019-08-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1063','Aadhya Kapoor','aadhya.kapoor@fintechco.com','Risk Analyst',11,12,'FINEMP1004','2021-10-27');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1064','Saanvi Nair','saanvi.nair@fintechco.com','Risk Analyst',11,24,'FINEMP1004','2021-05-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1065','Myra Garg','myra.garg@fintechco.com','Blockchain Developer',8,24,'FINEMP1004','2019-03-28');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1066','Diya Iyer','diya.iyer@fintechco.com','Sales Manager',1,12,'FINEMP1008','2020-12-19');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1067','Shaurya Chopra','shaurya.chopra@fintechco.com','Compliance Officer',9,24,'FINEMP1001','2021-10-06');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1068','Shaurya Singh','shaurya.singh@fintechco.com','Data Scientist',10,12,'FINEMP1002','2024-02-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1069','Vivaan Saxena','vivaan.saxena@fintechco.com','Risk Analyst',11,24,'FINEMP1003','2018-04-21');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1070','Saanvi Banerjee','saanvi.banerjee@fintechco.com','Credit Officer',2,23,'FINEMP1000','2020-12-24');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1071','Vivaan Verma','vivaan.verma@fintechco.com','Credit Officer',2,11,'FINEMP1008','2019-03-21');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1072','Saanvi Gupta','saanvi.gupta@fintechco.com','QA Engineer',5,11,'FINEMP1003','2019-11-08');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1073','Diya Nair','diya.nair@fintechco.com','Relationship Manager',1,25,'FINEMP1004','2024-08-22');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1074','Vihaan Chopra','vihaan.chopra@fintechco.com','Relationship Manager',1,1,'FINEMP1005','2024-09-10');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1075','Ananya Khan','ananya.khan@fintechco.com','QA Engineer',5,1,'FINEMP1009','2019-05-14');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1076','Avni Chowdhury','avni.chowdhury@fintechco.com','Credit Officer',2,25,'FINEMP1008','2022-01-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1077','Krishna Nair','krishna.nair@fintechco.com','UX Designer',13,1,'FINEMP1004','2019-12-07');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1078','Prisha Chopra','prisha.chopra@fintechco.com','Data Analyst',10,24,'FINEMP1001','2023-08-01');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1079','Krishna Iyer','krishna.iyer@fintechco.com','Financial Analyst',2,22,'FINEMP1000','2023-10-05');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1080','Avni Reddy','avni.reddy@fintechco.com','Data Analyst',10,23,'FINEMP1000','2021-02-24');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1081','Sakshi Malhotra','sakshi.malhotra@fintechco.com','Credit Officer',2,1,'FINEMP1004','2019-06-09');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1082','Vihaan Chowdhury','vihaan.chowdhury@fintechco.com','Financial Analyst',2,11,'FINEMP1005','2018-07-22');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1083','Krishna Malhotra','krishna.malhotra@fintechco.com','Sales Manager',1,23,'FINEMP1001','2022-12-26');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1084','Saanvi Chowdhury','saanvi.chowdhury@fintechco.com','Business Analyst',3,23,'FINEMP1004','2023-06-22');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1085','Aadhya Mehta','aadhya.mehta@fintechco.com','QA Engineer',5,24,'FINEMP1000','2021-10-11');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1086','Diya Iyer','diya.iyer@fintechco.com','Data Analyst',10,24,'FINEMP1006','2018-11-28');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1087','Avni Nair','avni.nair@fintechco.com','Relationship Manager',1,11,'FINEMP1008','2021-10-06');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1088','Avni Chowdhury','avni.chowdhury@fintechco.com','Customer Support',6,25,'FINEMP1005','2020-11-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1089','Aarav Joshi','aarav.joshi@fintechco.com','Security Engineer',8,24,'FINEMP1003','2021-03-01');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1090','Arjun Chowdhury','arjun.chowdhury@fintechco.com','Software Engineer',8,11,'FINEMP1007','2022-07-30');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1091','Diya Desai','diya.desai@fintechco.com','Compliance Officer',9,11,'FINEMP1008','2022-03-23');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1092','Ananya Nair','ananya.nair@fintechco.com','HR Manager',7,11,'FINEMP1003','2019-11-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1093','Shaurya Sharma','shaurya.sharma@fintechco.com','Product Manager',12,1,'FINEMP1002','2024-07-28');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1094','Aarav Kapoor','aarav.kapoor@fintechco.com','UX Designer',13,24,'FINEMP1007','2023-06-29');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1095','Ananya Khan','ananya.khan@fintechco.com','QA Engineer',5,25,'FINEMP1008','2021-03-12');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1096','Krishna Bhat','krishna.bhat@fintechco.com','Credit Officer',2,25,'FINEMP1003','2022-03-25');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1097','Sakshi Kapoor','sakshi.kapoor@fintechco.com','Marketing Manager',4,11,'FINEMP1000','2018-02-10');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1098','Arjun Patel','arjun.patel@fintechco.com','Risk Analyst',11,12,'FINEMP1004','2018-11-26');
INSERT INTO employee(employee_id,full_name,email,role,department_id,location_id,manager_id,date_of_joining)
VALUES ('FINEMP1099','Shaurya Chowdhury','shaurya.chowdhury@fintechco.com','DevOps Engineer',8,1,'FINEMP1008','2020-07-28');
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1000',1332478.37);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1001',1491158.23);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1002',1448927.95);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1003',519865.26);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1004',1922205.04);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1005',1085205.18);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1006',660681.91);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1007',1149019.58);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1008',370315.98);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1009',309717.04);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1010',1201969.11);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1011',1129637.9);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1012',1703783.22);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1013',759800.28);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1014',467884.86);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1015',1074426.0);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1016',1876390.13);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1017',526736.68);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1018',480639.52);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1019',443210.71);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1020',969422.69);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1021',1940128.43);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1022',1392523.21);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1023',1154429.09);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1024',611560.84);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1025',340969.05);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1026',1836299.49);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1027',1710679.64);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1028',1343177.54);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1029',1128053.06);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1030',436056.24);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1031',1363418.93);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1032',1069322.39);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1033',1513021.23);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1034',1243560.93);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1035',1507283.59);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1036',1875290.4);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1037',403990.23);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1038',1152589.39);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1039',1246312.4);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1040',1039818.46);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1041',1703490.23);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1042',1785167.47);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1043',849227.01);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1044',667541.44);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1045',911824.83);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1046',865704.81);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1047',1858162.08);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1048',1386670.96);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1049',1447037.81);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1050',865633.34);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1051',1064443.02);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1052',1673343.38);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1053',1502270.01);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1054',1675521.46);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1055',745459.27);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1056',685364.51);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1057',1641119.13);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1058',1098952.83);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1059',1430154.39);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1060',1258070.34);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1061',1349620.28);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1062',1641718.19);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1063',1833641.2);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1064',1809813.11);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1065',1947873.28);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1066',1333935.56);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1067',368244.88);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1068',1803057.99);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1069',1596298.88);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1070',1872784.84);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1071',1643988.07);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1072',1333187.28);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1073',1416536.32);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1074',1938308.68);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1075',687174.91);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1076',589221.29);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1077',1477253.1);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1078',1438958.04);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1079',1507078.74);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1080',400948.72);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1081',1113984.52);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1082',1036719.56);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1083',1413177.7);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1084',1982774.95);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1085',1026240.03);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1086',1950772.9);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1087',1333720.85);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1088',614347.62);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1089',330010.27);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1090',454938.59);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1091',1262938.4);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1092',512211.07);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1093',1325752.2);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1094',1373465.39);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1095',305337.03);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1096',807527.48);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1097',1468652.84);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1098',1521060.31);
INSERT INTO employee_compensation(employee_id,salary) VALUES ('FINEMP1099',586137.55);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1000',22,11);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1001',8,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1002',21,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1003',12,5);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1004',21,10);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1005',4,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1006',11,10);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1007',11,10);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1008',7,5);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1009',10,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1010',10,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1011',24,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1012',13,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1013',8,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1014',17,8);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1015',1,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1016',28,5);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1017',20,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1018',29,17);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1019',11,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1020',24,13);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1021',23,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1022',9,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1023',16,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1024',29,8);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1025',18,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1026',14,13);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1027',4,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1028',20,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1029',23,11);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1030',25,13);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1031',6,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1032',29,24);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1033',8,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1034',26,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1035',21,11);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1036',17,10);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1037',19,19);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1038',4,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1039',10,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1040',8,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1041',7,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1042',16,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1043',17,14);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1044',9,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1045',14,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1046',19,17);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1047',24,24);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1048',14,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1049',13,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1050',25,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1051',26,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1052',0,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1053',7,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1054',21,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1055',11,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1056',2,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1057',10,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1058',8,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1059',12,12);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1060',6,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1061',9,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1062',17,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1063',8,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1064',0,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1065',6,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1066',24,10);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1067',0,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1068',6,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1069',21,12);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1070',17,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1071',0,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1072',15,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1073',0,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1074',6,5);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1075',6,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1076',27,26);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1077',8,5);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1078',24,1);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1079',20,11);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1080',14,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1081',25,18);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1082',18,7);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1083',25,21);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1084',5,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1085',6,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1086',2,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1087',19,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1088',15,0);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1089',4,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1090',23,9);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1091',19,3);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1092',4,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1093',12,9);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1094',24,2);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1095',18,4);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1096',8,6);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1097',18,14);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1098',19,9);
INSERT INTO employee_leave(employee_id,leave_balance,leaves_taken) VALUES ('FINEMP1099',12,3);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1000',99.31);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1001',85.15);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1002',86.31);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1003',84.34);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1004',86.03);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1005',82.77);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1006',96.49);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1007',82.97);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1008',96.92);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1009',90.29);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1010',99.98);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1011',97.41);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1012',97.57);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1013',99.38);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1014',87.03);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1015',86.84);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1016',85.52);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1017',88.24);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1018',89.53);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1019',87.92);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1020',94.35);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1021',83.76);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1022',81.41);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1023',80.64);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1024',91.43);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1025',84.73);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1026',86.13);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1027',96.01);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1028',96.85);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1029',97.48);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1030',90.6);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1031',84.54);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1032',96.83);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1033',97.62);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1034',97.76);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1035',80.39);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1036',91.5);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1037',99.74);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1038',92.5);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1039',90.36);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1040',94.28);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1041',90.84);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1042',89.15);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1043',91.97);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1044',88.61);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1045',99.1);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1046',94.1);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1047',86.19);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1048',98.85);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1049',85.89);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1050',97.9);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1051',80.35);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1052',80.95);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1053',91.65);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1054',84.17);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1055',91.63);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1056',99.67);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1057',92.5);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1058',96.31);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1059',93.02);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1060',98.75);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1061',81.37);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1062',96.07);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1063',85.81);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1064',83.64);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1065',81.24);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1066',91.78);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1067',80.02);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1068',81.1);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1069',96.61);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1070',95.36);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1071',98.33);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1072',97.66);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1073',95.13);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1074',92.42);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1075',87.01);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1076',88.76);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1077',97.75);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1078',90.49);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1079',87.41);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1080',81.49);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1081',80.71);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1082',93.4);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1083',91.85);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1084',99.17);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1085',92.28);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1086',88.26);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1087',90.98);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1088',98.8);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1089',82.24);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1090',91.15);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1091',86.4);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1092',85.19);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1093',93.73);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1094',91.59);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1095',88.06);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1096',97.67);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1097',94.91);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1098',92.26);
INSERT INTO employee_attendance(employee_id,attendance_pct) VALUES ('FINEMP1099',95.52);
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1000',3,'2024-05-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1001',5,'2024-01-20');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1002',2,'2025-02-11');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1003',1,'2024-07-24');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1004',3,'2024-01-12');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1005',2,'2024-09-15');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1006',2,'2024-02-26');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1007',4,'2024-01-31');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1008',5,'2024-08-07');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1009',2,'2025-04-22');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1010',5,'2024-04-20');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1011',5,'2024-01-07');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1012',3,'2024-11-28');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1013',1,'2024-11-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1014',3,'2024-06-18');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1015',4,'2024-07-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1016',5,'2025-03-16');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1017',1,'2025-04-10');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1018',5,'2024-05-09');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1019',5,'2024-12-20');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1020',1,'2024-09-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1021',1,'2025-03-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1022',1,'2025-03-31');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1023',2,'2024-01-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1024',2,'2025-01-17');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1025',3,'2024-04-05');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1026',1,'2024-12-12');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1027',1,'2024-06-08');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1028',4,'2025-03-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1029',2,'2025-02-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1030',5,'2024-02-07');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1031',5,'2024-12-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1032',1,'2024-01-20');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1033',1,'2024-10-09');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1034',2,'2024-09-08');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1035',3,'2025-04-04');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1036',4,'2024-07-05');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1037',5,'2024-01-10');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1038',4,'2024-05-13');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1039',5,'2024-10-24');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1040',3,'2024-03-24');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1041',1,'2024-07-30');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1042',4,'2025-04-28');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1043',4,'2024-02-16');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1044',5,'2024-09-13');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1045',4,'2025-02-05');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1046',1,'2024-04-13');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1047',5,'2025-03-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1048',3,'2024-07-31');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1049',5,'2024-02-01');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1050',1,'2024-05-17');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1051',4,'2025-04-15');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1052',4,'2024-06-08');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1053',5,'2024-05-12');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1054',1,'2024-06-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1055',1,'2024-03-07');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1056',2,'2024-06-24');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1057',2,'2024-06-07');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1058',5,'2025-01-31');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1059',2,'2025-04-25');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1060',4,'2024-09-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1061',3,'2024-01-19');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1062',1,'2025-03-09');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1063',2,'2024-06-29');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1064',2,'2024-05-17');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1065',2,'2024-10-03');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1066',1,'2025-01-09');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1067',3,'2024-05-01');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1068',3,'2024-11-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1069',4,'2024-09-28');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1070',2,'2024-02-04');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1071',2,'2024-10-15');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1072',3,'2024-07-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1073',5,'2025-01-29');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1074',3,'2025-04-12');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1075',5,'2025-04-27');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1076',4,'2024-02-25');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1077',1,'2024-08-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1078',2,'2024-02-28');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1079',3,'2024-01-22');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1080',5,'2024-12-08');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1081',3,'2024-07-26');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1082',2,'2024-01-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1083',1,'2024-01-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1084',2,'2024-06-10');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1085',2,'2024-12-19');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1086',5,'2024-03-21');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1087',2,'2024-05-16');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1088',5,'2024-04-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1089',1,'2024-10-29');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1090',1,'2024-09-26');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1091',1,'2024-08-30');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1092',3,'2024-05-18');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1093',5,'2024-01-31');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1094',2,'2024-10-23');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1095',5,'2024-02-15');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1096',3,'2024-01-04');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1097',2,'2024-05-14');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1098',4,'2024-08-06');
INSERT INTO employee_performance(employee_id,performance_rating,last_review_date)
VALUES ('FINEMP1099',3,'2024-11-09');


INSERT INTO table_access_roles VALUES
('employee','HR'),
('employee','Admin'),

('employee_compensation','Finance'),
('employee_compensation','HR'),
('employee_compensation','Admin'),

('employee_performance','Managers'),
('employee_performance','HR'),
('employee_performance','Admin'),

('employee_leave','HR'),
('employee_leave','Employees'),
('employee_leave','Admin'),

('employee_attendance','HR'),
('employee_attendance','Managers'),
('employee_attendance','Admin'),

('departments','Admin'),
('departments','HR'),
('departments','Managers'),

('locations','Admin'),
('locations','HR'),
('locations','Managers');



INSERT INTO users (user_id, employee_id, password, user_role)
SELECT
    email                                    AS user_id,
    employee_id,
    lower(split_part(full_name, ' ', 2)) || '_' || extract(year FROM date_of_joining)     AS password,

    CASE
        -- Finance
        WHEN role ILIKE '%financial%'
          OR role ILIKE '%credit%'
          OR role ILIKE '%treasury%'
          OR role ILIKE '%risk%'
        THEN 'finance'

        -- Marketing
        WHEN role ILIKE '%marketing%'
          OR role ILIKE '%sales%'
        THEN 'marketing'

        -- HR
        WHEN role ILIKE '%hr%'
        THEN 'hr'

        -- Engineering
        WHEN role ILIKE '%engineer%'
          OR role ILIKE '%developer%'
          OR role ILIKE '%devops%'
          OR role ILIKE '%qa%'
          OR role ILIKE '%software%'
          OR role ILIKE '%data%'
        THEN 'engineering'

        -- C-Level / Managers
        WHEN role ILIKE '%manager%'
        THEN 'Managers'

        -- Default Employee
        ELSE 'general'
    END AS user_role

FROM employee
ON CONFLICT (user_id) DO NOTHING;


COMMIT;