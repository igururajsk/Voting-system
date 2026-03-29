-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2023 at 08:57 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `votingsystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `facerec`
--

CREATE TABLE `facerec` (
  `usernames` varchar(50) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `Uniquepass` varchar(50) DEFAULT NULL,
  `Userids` varchar(50) DEFAULT NULL,
  `Votercardnos` varchar(50) DEFAULT NULL,
  `emails` varchar(50) DEFAULT NULL,
  `phonenos` varchar(11) DEFAULT NULL,
  `Adresess` varchar(50) DEFAULT NULL,
  `LoginAuth` varchar(5) DEFAULT NULL,
  `FaceAuth` varchar(5) DEFAULT NULL,
  `VoteAuth` varchar(5) DEFAULT NULL,
  `Constituency` varchar(50) NOT NULL,
  `f_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `facerec`
--

INSERT INTO `facerec` (`usernames`, `password`, `Uniquepass`, `Userids`, `Votercardnos`, `emails`, `phonenos`, `Adresess`, `LoginAuth`, `FaceAuth`, `VoteAuth`, `Constituency`, `f_id`) VALUES
('abhi', '1234', '64Ozp-\\lm=nK0', '12345', '123456', 'itsmeabhishekb5@gmail.com', '9036251478', 'bangalore', 'yes', 'yes', 'yes', 'Dasarahalli', 1),
('manju', '9090', 'da\'iXVI/F', '9091', '9092', 'manjunathgp1243@gmail.com', '9035560799', 'mysore', 'yes', 'yes', 'no', 'Malleshwara', 5);

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

CREATE TABLE `result` (
  `bjp` int(10) DEFAULT NULL,
  `congress` int(10) DEFAULT NULL,
  `jds` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `result`
--

INSERT INTO `result` (`bjp`, `congress`, `jds`) VALUES
(3, 4, 1);

--
-- Indexes for dumped tables
--

--
/
