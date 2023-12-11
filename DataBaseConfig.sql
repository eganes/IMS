CREATE DATABASE IMS;
USE IMS;

CREATE TABLE Accounts (
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100),
    Role ENUM('admin', 'user', 'agent') NOT NULL,
    DateCreated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender ENUM('male', 'female', 'other'),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(15),
    Address VARCHAR(255)
);

CREATE TABLE Policies (
    PolicyID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    PolicyType VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Premium DECIMAL(10, 2),
    Status ENUM('active', 'expired', 'cancelled'),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Claims (
    ClaimID INT AUTO_INCREMENT PRIMARY KEY,
    PolicyID INT,
    DateOfClaim DATE,
    Description TEXT,
    Amount DECIMAL(10, 2),
    Status ENUM('submitted', 'processed', 'rejected', 'approved'),
    FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
);

CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    PolicyID INT,
    DateOfPayment DATE,
    Amount DECIMAL(10, 2),
    PaymentMethod ENUM('credit_card', 'debit_card', 'bank_transfer'),
    FOREIGN KEY (PolicyID) REFERENCES Policies(PolicyID)
);
