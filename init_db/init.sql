-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS ocs_subscribers_db;
USE ocs_subscribers_db;

-- Crear la tabla account
CREATE TABLE IF NOT EXISTS account (
    account_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_type VARCHAR(50),
    balance BIGINT,
    creation_date DATE,
    grace_end_date DATE
);

-- Crear la tabla packages
CREATE TABLE IF NOT EXISTS packages (
    package_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    description VARCHAR(255),
    activation_date DATE,
    validity_period INTEGER,
    expiry_date DATE,
    data_balance BIGINT,
    qos_id INTEGER,
    priority INTEGER
);

-- Crear la tabla subscriber
CREATE TABLE IF NOT EXISTS subscriber (
    msisdn BIGINT PRIMARY KEY,
    account_id BIGINT,
    imsi VARCHAR(50),
    line_type VARCHAR(50),
    status VARCHAR(20),
    islocked BOOLEAN,
    FOREIGN KEY (account_id) REFERENCES account(account_id) ON DELETE CASCADE
);

-- Crear la tabla subscriber_packages
CREATE TABLE IF NOT EXISTS subscriber_packages (
    subscriber_packages_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    msisdn BIGINT,
    package_id BIGINT,
    FOREIGN KEY (msisdn) REFERENCES subscriber(msisdn) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE
);

-- Crear la tabla de compra de paquetes
CREATE TABLE IF NOT EXISTS package_purchase (
    purchase_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    validity_period INT,
    data_balance BIGINT,
    price INT,
    type TEXT,
    qos_id INT,
    priority INT DEFAULT 1
);

-- Insertar datos en la tabla account
INSERT INTO account (account_id, account_type, balance, creation_date, grace_end_date) VALUES
(1, 'prepaid', 5000, '2024-01-01', '2024-12-31'),
(2, 'm2m', 2000, '2024-02-10', '2025-01-10'),
(3, 'prepaid', 8000, '2023-12-15', '2024-11-30');

-- Insertar datos en la tabla packages
INSERT INTO packages (package_id, name, description, activation_date, validity_period, expiry_date, data_balance, qos_id, priority) VALUES
(101, 'Plan Básico', '1GB de datos', '2024-03-01', 30, '2024-03-31', 1073741824, 1, 1),
(102, 'Plan Avanzado', '5GB de datos', '2024-03-05', 30, '2024-04-05', 5368709120, 2, 2),
(103, 'Plan Ilimitado', 'Datos ilimitados', '2024-03-10', 30, '2024-04-10', 53687091200, 3, 3);

-- Insertar datos en la tabla subscriber
INSERT INTO subscriber (msisdn, account_id, imsi, line_type, status, islocked) VALUES
(51914389110, 1, '716001000000124', 'prepaid', 'active', FALSE),
(51976543210, 2, '716001000000125', 'postpaid', 'active', FALSE),
(51965432109, 3, '716001000000126', 'prepaid', 'active', FALSE);

-- Insertar datos en la tabla subscriber_packages
INSERT INTO subscriber_packages (msisdn, package_id) VALUES
(51914389110, 101),
(51976543210, 102),
(51965432109, 103);

-- Insertar datos en la tabla package_purchase
INSERT INTO package_purchase (name, description, validity_period, data_balance, price, type, qos_id)
VALUES
('Plan Básico', '1GB de datos', 30, 1073741824, 1000, 'prepaid' , 1),
('Plan Avanzado', '5GB de datos', 30, 5368709120, 1500,'prepaid', 1),
('Plan Ilimitado', 'Datos ilimitados', 30, 53687091200, 2000,'prepaid', 1);
