# 🚘 GC Rental - Car Rental Management System

## Read Me - User and Programmer Documentation

## 1. Purpose of the Application

The GC Rental App is a car rental management system which is a console base application developed in Python to manage vehicle rentals efficiently. The system allows customer to browse and book vehicles, administrators to manage vehicles and bookings, and a super administrator to create admin accounts.

THe application has structured system design, role-based access control, database integration, and layered architecture.


## 2. System Requirement

To run this system, you need:

* Python 3.10 or higher
* Install all the dependencies included in requirements.txt file
* SQLite (automatically handled by Python)
* Operating Systems: macOS, Windows or Linux


## 3. Installation and Configuration Guide

Follow the steps below to configure and run the system

### Step 1: Extract the Project

Download and extract the project folder to your local machine.

### Step 2: Verify Python Installation

Open a terminal and run: `python3 --version`

Ensure Python 3.10 or above is installed. Prefer Python version 3.14

You can download the latest Python version from:
https://www.python.org/downloads/

### Step 3: Create Virtual Environment 

It is recommended to use a Python virtual environment to isolate project dependencies.

First cd in to the `GCRental` project folder. Then follow the instructions below based on the OS you are using.

### On Windows:

* Run this command to setup virtual environment
`python -m venv venv`

* Activate it
`venv\scripts\activate`

### On macOS / Linux:

* Run this command
`python3 -m venv venv`

* Activate it:
`source venv/bin/activate`

### Step 4: Install Required Dependencies

Use the given requirements.txt file and install dependencies using:
`pip install -r requirements.txt`

### Step 5: Run the Application

Use the terminal and cd into `gc_rental_app` application folder.
Then run the following command:
`python main.py`

### Step 6: Database Initialization
* When the system runs for the first time, the SQLite database file is automatically created.
* Required tables are generated automatically.
* The default Super Admin account is inserted into the database.

*No manual database configuration is required.

## 4. Operating the System

When the application starts, the main menu provides the following options:
* Login
* Register
* Exit

New customer must register before logging in (except the predefined super Admin).
You need to create at least one `admin` account to manage car rentals. Admin accounts can only be created by the Super Admin. Super admin login details mentioned in the next section. 
Once created logout from super admin and login back as the admin


## 5. Default Super Admin Account

The system automatically creates a Super Admin Account Directly in the database during initialization.

You must use the following credentials to login in as Super admin:

Username: superadmin
Password: 1234


## 6. User Roles and Functionalities

### Super Admin

The super admin can just create admins so that admins can manage the vehicles and bookings for the system.

### Admin

Admin manage vehicles and bookings.

Initial menu presented to Admin will have following options:
* Manage Cars
* Manage Bookings
* Logout

#### Manage Cars:

* Add New Cars
* Update Car Details
* Remove Car
* View All Cars
* Go Back

#### Manage Bookings:

* View All Bookings
* Manage Pending Bookings
* Complete Booking
* Go Back

Admin can either `Approve` or `Reject` any pending bookings
Once approved vehicle will be allocated to the user for the given period
If cancelled vehicle will be put back to the pool so user can continue booking.
Once the vehicle is returned after the booking period Admin will complete the booking by adding any additional chargers and booking chargers.

### Customer

Customer can browse and book any vehicle that is not already book for the selected period.

Initial menu presented to the customer will have following options:

* Book a Car
* View My Bookings
* Logout

#### Booking Rules:
* User need to enter the expected start date and end date to see all the cars that is available to book within that period.
* Once the vehicle is decided from the list user can continue for booking that
* When providing the booking details user allowed to change the start date and end date if wanted but it is subjected to the availability.
* Start date provided cannot be a past day
* End date must be later than start date
* Rental period must be within allowed minimum and maximum limits

If any condition is not met, the system will display an appropriate message.

#### Booking Status Types
* PENDING - Once has book a car and awaiting Approval from Admin
* CONFIRMED - Approved by Admin
* REJECTED - Rejected by Admin
* COMPLETED - Rental finished

## 7. Logging Out and Exiting
* User can log out from their respective main menu.
* After logging out, the application can be existed from the main menu.

## 8. Error Messages

The system will show suitable error messages in every where which is needed including following scenarios:

* Login credentials are incorrect
* Booking dates are invalid
* Rental period exceeds allowed limits
* Vehicle is unavailable
* User attempts an action without permission
* etc.

## 9. Error Logging

The GC Car Rental system includes an internal logging mechanism to record system errors.

If an unexpected error occurs during any of the action, the details of the error are automatically written to a log file. This helps in identifying and troubleshooting issues without interrupting normal system usage.

* Errors are recorded in a log file stored in the project directory.
* Normal users do not need to interact with the log file.
* The log file is mainly used for debugging and system maintenance purposes.

If the system behaves unexpectedly, administrators can check the log file to review the recorded error information or can be passed to the developers for further analysis.  

## 10. Project Structure and File Description

Below is the general structure of the project folder:

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

File Purpose Overview

* main.py - Entry point of the application
* session.py - Manages the user login session
* database/ - Database connection and configuration
* repository Module - Handle SQL operation and data access
* service module - Contains business logic, validations and error handling
>>>>>>>>>>>>>>>>>>>>>>>>>>>

## 11. Software License Agreement

This project is released under the MIT License.

The MIT License permits anyone to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that the original copyright notice and license are included.

The software is provided "as is", without warranty of any kind.

For full license terms, refer to the LICENSE file included in this project.

## 12. Known Issues and Limitations

* The system does not support concurrent user access.
* The application is console-based only (no graphical interface).
* No automated email or notification mechanism implemented

*These limitations do not affect core system functionality

## Credits

Developer: Pallage Ganuke Achiranath Perera
Student ID: 270842427
Course: Master of Software Engineering
Institution: YooBee College
Year: 2026



 


