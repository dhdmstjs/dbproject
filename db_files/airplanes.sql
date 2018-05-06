-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 06, 2018 at 02:57 PM
-- Server version: 5.7.19
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airplanes`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY (`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('American Airlines'),
('China Eastern'),
('Delta'),
('Korean Air');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

DROP TABLE IF EXISTS `airline_staff`;
CREATE TABLE IF NOT EXISTS `airline_staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY (`username`),
  KEY `airline_name` (`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('dirty_dan@gmail.com', '71038f91e38dcf922c59fe7a53720ed7:a29a42e8d3ee45178dae050082df2f92', 'Daniela', 'Oh', '2018-05-01', 'Korean Air');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` varchar(11) NOT NULL,
  `seats` int(11) NOT NULL,
  PRIMARY KEY (`airline_name`,`airplane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('American Airlines', '00000', 120),
('American Airlines', '11111', 60),
('American Airlines', '33322', 220),
('China Eastern', '12345', 200),
('China Eastern', '54321', 150),
('Delta', '11111', 100),
('Delta', '12345', 200),
('Delta', '141523', 100),
('Korean Air', '151451', 100),
('Korean Air', '22222', 160),
('Korean Air', '56789', 60);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL,
  PRIMARY KEY (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('ABQ', 'Albuquerque'),
('ATL', 'Atlanta'),
('CDG', 'Paris'),
('JFK', 'New York'),
('LHR', 'London'),
('ORD', 'Chicago'),
('PEK', 'Beijing'),
('PVG', 'Shanghai'),
('SFO', 'San Francisco');

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

DROP TABLE IF EXISTS `booking_agent`;
CREATE TABLE IF NOT EXISTS `booking_agent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `booking_agent_id` varchar(11) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('c', 'e5efc4e8513e7dd6c1f36413e18c1cf3:29d439afacc64b029ad10f5d353617b5', '1234561'),
('SalesMcGee@hotmail.com', 'pass', '4321');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `building_number` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `passport_number` varchar(30) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('colton@nyu', 'noname', 'c1b70c81e392047d70f194bd1e545094:8df19990bf724b7b92d2438623f69375', 'test', 'test', 'test', 'test', 'test', 'test', '2020-04-01', 'test', '1996-02-09'),
('fake_customer', 'bob', 'pass', 'test', 'test', 'test', 'test', 'test', 'test', '2026-02-05', 'test', '1996-04-05');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_num` varchar(11) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` varchar(11) NOT NULL,
  PRIMARY KEY (`airline_name`,`flight_num`),
  KEY `airline_name` (`airline_name`,`airplane_id`),
  KEY `departure_airport` (`departure_airport`),
  KEY `arrival_airport` (`arrival_airport`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('American Airlines', '00011', 'JFK', '2018-06-12 21:40:00', 'ATL', '2018-06-12 23:40:00', '181', 'delayed', '33322'),
('American Airlines', '01010', 'ORD', '2018-08-05 12:20:00', 'PVG', '2018-08-06 06:00:00', '1200', 'on-time', '11111'),
('American Airlines', '01011', 'ORD', '2018-08-06 12:20:00', 'PVG', '2018-08-07 06:00:00', '1200', 'on-time', '00000'),
('American Airlines', '10101', 'JFK', '2018-06-15 21:40:00', 'ATL', '2018-06-15 21:44:00', '181', 'on-time', '33322'),
('American Airlines', '14141', 'JFK', '2018-05-09 00:07:00', 'ATL', '2018-05-24 01:05:00', '121', 'delayed', '33322'),
('American Airlines', '141411', 'JFK', '2018-05-09 00:07:00', 'ATL', '2018-05-24 01:05:00', '121', 'delayed', '33322'),
('American Airlines', '54321', 'ATL', '2018-06-13 02:10:00', 'CDG', '2018-06-13 13:20:00', '910', 'on-time', '00000'),
('American Airlines', '99888', 'ORD', '2018-12-30 20:00:00', 'LHR', '2018-12-31 00:20:00', '526', 'on-time', '33322'),
('China Eastern', '12121', 'PEK', '2018-06-05 18:00:00', 'ORD', '2018-06-05 21:00:00', '330', 'on-time', '12345'),
('China Eastern', '98765', 'PVG', '2018-02-10 12:00:00', 'JFK', '2018-05-11 14:00:00', '940', 'landed', '54321'),
('Delta', '12321', 'ATL', '2018-04-11 10:30:00', 'JFK', '2018-04-11 13:00:00', '150', 'landed', '11111'),
('Delta', '98765', 'JFK', '2018-05-11 12:00:00', 'ORD', '2018-05-11 18:00:00', '200', 'on-time', '12345'),
('Korean Air', '22234', 'CDG', '2019-01-10 06:00:00', 'LHR', '2019-01-10 10:00:00', '400', 'crashed', '56789'),
('Korean Air', '43434', 'JFK', '2018-09-11 10:35:00', 'CDG', '2018-09-11 19:40:00', '800', 'on-time', '22222');

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
CREATE TABLE IF NOT EXISTS `purchases` (
  `ticket_id` varchar(11) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` varchar(11) DEFAULT NULL,
  `purchase_date` date NOT NULL,
  PRIMARY KEY (`ticket_id`,`customer_email`),
  KEY `customer_email` (`customer_email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
('00001', 'fake_customer', '1234561', '2018-05-05'),
('00014', 'colton@nyu', '1234561', '2018-01-02'),
('00424', 'colton@nyu', '1234561', '2018-05-04'),
('01404', 'colton@nyu', NULL, '2018-01-12'),
('06503', 'colton@nyu', NULL, '2018-05-02'),
('07801', 'fake_customer', '4321', '2018-05-01'),
('10002', 'colton@nyu', NULL, '2018-05-06'),
('34003', 'colton@nyu', NULL, '2018-05-06'),
('64203', 'fake_customer', '4321', '2018-05-05');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticket_id` varchar(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_num` varchar(11) NOT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `airline_name` (`airline_name`,`flight_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
('00036', 'American Airlines', '01010'),
('00335', 'American Airlines', '01010'),
('03302', 'American Airlines', '01010'),
('05354', 'American Airlines', '01010'),
('06501', 'American Airlines', '01010'),
('45303', 'American Airlines', '01010'),
('01036', 'American Airlines', '01011'),
('01136', 'American Airlines', '01011'),
('02236', 'American Airlines', '01011'),
('05606', 'American Airlines', '54321'),
('13101', 'American Airlines', '54321'),
('24202', 'American Airlines', '54321'),
('64204', 'American Airlines', '54321'),
('64303', 'American Airlines', '54321'),
('98705', 'American Airlines', '54321'),
('00904', 'American Airlines', '99888'),
('11101', 'American Airlines', '99888'),
('15405', 'American Airlines', '99888'),
('42403', 'American Airlines', '99888'),
('98702', 'American Airlines', '99888'),
('00655', 'China Eastern', '12121'),
('01102', 'China Eastern', '12121'),
('01404', 'China Eastern', '12121'),
('07801', 'China Eastern', '12121'),
('99003', 'China Eastern', '12121'),
('00424', 'China Eastern', '98765'),
('10002', 'China Eastern', '98765'),
('34003', 'China Eastern', '98765'),
('52005', 'China Eastern', '98765'),
('60001', 'China Eastern', '98765'),
('00014', 'Delta', '12321'),
('00401', 'Delta', '12321'),
('00602', 'Delta', '12321'),
('00903', 'Delta', '12321'),
('05005', 'Delta', '12321'),
('00001', 'Delta', '98765'),
('00013', 'Delta', '98765'),
('00202', 'Delta', '98765'),
('02005', 'Delta', '98765'),
('09004', 'Delta', '98765'),
('00104', 'Korean Air', '22234'),
('00221', 'Korean Air', '22234'),
('00402', 'Korean Air', '22234'),
('06503', 'Korean Air', '22234'),
('32202', 'Korean Air', '43434'),
('52301', 'Korean Air', '43434'),
('52504', 'Korean Air', '43434'),
('64203', 'Korean Air', '43434');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`,`airplane_id`) REFERENCES `airplane` (`airline_name`, `airplane_id`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`airport_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`airport_name`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`),
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_num`) REFERENCES `flight` (`airline_name`, `flight_num`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
