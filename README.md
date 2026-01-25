# 🚘 GC Rental App

## User Documentation

## 1. Overview

The GC Rental App is a car rental management system which is a console base application that allows users to manage vehicle rentals through a simple text interface.

The current version of the app support three types of users:

* Super Admin
* Admin
* Customer

Each user type has different permission and access levels.

This document explains how to install, run and use the system.


## 2. System Requirement

To run this system, you need:

* Python 3.x installed
* Install all the dependencies included in requirements.txt file
* SQLite (automatically handled by Python)


## 3. How to Run the System

1. Download the unzip the file given or clone the project directly from git hub link provided.
2. Open a terminal inside the project folder.
3. Run the following command:

`python main.py`

4. The system will start and display the main menu.

THe database will be created automatically if it does not already exist.

## 4. Default Super Admin Account

The system automatically creates a Super Admin Account Directly in the database during initialization.

You must use the following credentials to login in as Super admin:

Username: superadmin
Password: 1234

## 5. Main Menu Options

When the application starts, users can:

* Login
* Register
* Exit

New users must register before logging in except for the Super Admin.

## 6. User Roles and Functionalities

### Super Admin

The super admin can just create admins so that admins can manage the vehicles and bookings of the system.

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

 


