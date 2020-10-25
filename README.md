# SchedulerWebsite

## Brief description of the project
	This is an app that helps manage scheduling for independent freelancers, mostly suited for psychologists, lawyers, consultants or other professionals working on appointments with fixed durations. Users can view, add, edit or delete appointments. Users have to sign up in order to access the app's functionalities. As a future development, it will offer descriptive statistics, data visualization and predictive analytics.
## Main system functions
	- login panel
	- admin ?
	- User
		- Registration process: login after email confirmation (confirmation link active for limited time)
		- View/Modify appointments calendar
			- This week's appointments (default view)
			- Change week to view
			- Monthly view, daily view
		- 
## Basic entities (Models)
	- Admin ?
	- Users
		- UserID (PK): int
		- Name: str
		- Email: str
	- Guests ? - client with no account
	- Appointments
		- AppointmentID (PK): int
		- Date and time: DateTime
		- ClientID (FK)
		- Setting: Face to face / Online
	- Clients
		- ClientID (PK): int
		- Name: str
		- Problem: str
		- Notes: str
		- Appointment number: int (auto-increment)
		- Recurring: Bool
		- Price: int
		- Receipt: Bool
		- email: str
## Functionalities
	- Clients receive automatic reminders by email
## Future Developmentss
	- Waiting List
	- Taxes accounting
	- Predictive statistics: earning, nr of sessions, taxes etc. 
## Necessary Technologies and Integrations: Django, MySQL

