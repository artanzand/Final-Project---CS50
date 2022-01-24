Title: COVID-19 Testing – Online Booking Website Name: Artan Zandian Calgary, Alberta, Canada Dec 2020

See below for presentation: [YouTube Demo](https://youtu.be/VdjYeRtxZYI)

Languages used: Python, SQL, HTML, JavaScript, CSS

This website has been designed to reduce the pressure on Public Health call centres in Calgary, Alberta caused by higher than normal volumes related to COVID-19. The website serves three main purposes:

Screening of the patients: Through a self-assessment questionnaire, this module identifies whether a testing is required, and if so, directs the patient to the booking webpage. The information from the questionnaire along with the user ID is always saved in a database no matter if the user decides not to finalize the booking. This allows a broader population pulse check allowing for further studies to be done. The other benefit of this questionnaire is that it allows Public Health to drop selected appointments based on patient symptoms in order to create extra capacity for the lab (to reduce the turnaround).

Helping the patient book a time for walk-in or drive thru testing appointments (taking swabs): This section provides three location alternatives, and dates for the patient to choose from. Once selected, another form will be updated with available time slots for the patient according to the selected location and date. The maximum number of appointments per time slot per location has been limited to 3 to allow proof of concept with less input. As part of the proces, the patient can also provide a phone number which will be used to text the result. Once confirmed a unique booking code (calculated through a hash function) will be provided to the patient to modify the appointment if needed. The patient can alternatively log back in with name and Alberta Health credentials to book a new appointment.

Allowing the patient to cancel or modify the booked appointment: The booking code provided at the time of registration can be used to cancel the appointment or replace it with a new one. Using the booking code, the patient does not require to re-enter credential. The user id is automatically recognized when this code is entered, and subsequently, a new session is created to allow altering of the booking.

The patient needs to be logged in to get access to the first two steps. To access the Modify/Cancel section the patient will enter a booking code which confirms his identity and allows for the previous booking to be removed or replaced by a new one.

No registration is required to book an appointment. This website takes benefit from presence of a unique identifier call Alberta Health Number (AHN). AHN is an ID given to anyone who is born in Alberta or immigrates to the province within two-weeks of arrival. In absence of access to this database and for demonstration purposes, the people database has been downloaded from imdb and has been modified to reflect the minimum data required. The size of the database is roughly over a million entries which is about the size of the population in Calgary, AB.

Last but not the least, the website is set up to run in different sessions allowing for multiple patients to book appointments at the same time.
