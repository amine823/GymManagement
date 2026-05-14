CREATE DATABASE IF NOT EXISTS gym_management;
USE agence_voyage;

DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS subscription_plans;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS members;

CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('M', 'F', 'Other'),
    join_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Active', 'Inactive', 'Suspended') DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE subscription_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL UNIQUE,
    duration_months INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    plan_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    payment_status ENUM('Paid', 'Pending', 'Overdue') DEFAULT 'Pending',
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(plan_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Active', 'Inactive') DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    check_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    check_out_time DATETIME NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO subscription_plans (plan_name, duration_months, price, description) VALUES
('Monthly Basic', 1, 80, 'Basic gym access for 1 month'),
('Quarterly Standard', 3, 160, 'Standard gym access for 3 months with group classes'),
('Annual Premium', 12, 920, 'Full year access with all amenities and personal training'),
('Student Monthly', 1, 60, 'Discounted monthly plan for students'),
('VIP Yearly', 12, 1300, 'VIP access with personal trainer and spa facilities');

INSERT INTO members (first_name, last_name, email, phone, date_of_birth, gender, join_date, status) VALUES
('Ahmed', 'Ben Ali', 'ahmed.benali@email.com', '55568124', '2001-03-15', 'M', '2026-01-10', 'Active'),
('Fatma', 'Trabelsi', 'fatma.trabelsi@email.com', '92227086', '2000-07-22', 'F', '2026-02-15', 'Active'),
('Mohamed', 'Gharbi', 'mohamed.gharbi@email.com', '24108723', '2005-11-08', 'M', '2025-09-23', 'Active'),
('Amira', 'Jebali', 'amira.jebali@email.com', '29889745', '2003-05-30', 'F', '2025-02-10', 'Active'),
('Karim', 'Sassi', 'karim.sassi@email.com', '55675299', '1999-09-14', 'M', '2026-01-20', 'Suspended'),
('Leila', 'Hamdi', 'leila.hamdi@email.com', '52356745', '1998-12-25', 'F', '2025-03-25', 'Active'),
('Youssef', 'Mansour', 'youssef.mansour@email.com', '55789012', '1997-04-18', 'M', '2024-03-05', 'Active'),
('Nour', 'Khemiri', 'nour.khemiri@email.com', '24890123', '2001-08-07', 'F', '2026-04-10', 'Active'),
('Sami', 'Bouaziz', 'sami.bouaziz@email.com', '29901234', '2004-02-28', 'M', '2026-03-15', 'Suspended'),
('Meriem', 'Chaari', 'meriem.chaari@email.com', '55245336', '1999-06-12', 'F', '2025-10-12', 'Active');

INSERT INTO subscriptions (member_id, plan_id, start_date, end_date, payment_status) VALUES
(1, 3, '2026-01-10', '2027-01-10', 'Paid'),
(2, 2, '2026-02-15', '2026-05-15', 'Paid'),
(3, 1, '2025-09-23', '2025-10-23', 'Paid'),
(4, 4, '2025-02-10', '2025-03-10', 'Paid'),
(5, 1, '2026-01-20', '2026-02-20', 'Overdue'),
(6, 3, '2025-03-25', '2026-03-25', 'Paid'),
(7, 2, '2024-03-05', '2024-06-05', 'Paid'),
(8, 4, '2026-04-10', '2026-05-10', 'Pending'),
(9, 1, '2026-03-15', '2026-04-15', 'Overdue'),
(10, 5, '2025-10-12', '2026-10-12', 'Paid');

INSERT INTO trainers (first_name, last_name, specialization, email, phone, hire_date, status) VALUES
('Hichem', 'Ayari', 'Bodybuilding & Strength Training', 'hichem.ayari@gym.com', '92245689', '2024-01-15', 'Active'),
('Salma', 'Mejri', 'Yoga & Pilates', 'salma.mejri@gym.com', '55222333', '2025-03-22', 'Active'),
('Rami', 'Bouzid', 'CrossFit & HIIT', 'rami.bouzid@gym.com', '24563122', '2025-06-11', 'Active'),
('Ines', 'Ferchichi', 'Cardio & Weight Loss', 'ines.ferchichi@gym.com', '55586741', '2025-09-01', 'Active'),
('Bilel', 'Oueslati', 'Personal Training & Nutrition', 'bilel.oueslati@gym.com', '24632159', '2026-01-05', 'Active');

INSERT INTO attendance (member_id, check_in_time, check_out_time) VALUES
(1, '2026-01-11 08:00:00', '2026-01-11 09:30:03'),
(2, '2026-02-19 09:00:00', '2026-02-19 10:41:12'),
(3, '2025-09-23 10:00:00', '2025-09-23 11:32:45'),
(4, '2025-02-10 17:00:00', '2025-02-10 18:15:30'),
(6, '2026-01-20 18:00:00', '2026-01-20 19:52:06'),
(7, '2024-03-05 07:30:00', '2024-03-05 08:57:26'),
(8, '2026-04-10 08:30:00', '2026-04-10 10:01:00'),
(1, '2026-01-14 17:30:00', '2026-01-14 19:03:15'),
(2, '2026-02-22 18:00:00', '2026-02-22 19:33:09'),
(10, '2025-10-12 19:00:00', '2025-10-12 20:26:56'),
(1, '2026-01-19 08:00:00', '2026-01-19 09:02:50'),
(4, '2025-02-16 17:00:00', '2025-02-16 17:59:03'); 