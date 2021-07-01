-- Keep a log of any SQL queries you execute as you solve the mystery.

-- First have a look at the crime report
SELECT id, description FROM crime_scene_reports WHERE street = "Chamberlin Street" AND year = 2020 AND month = 07 AND day = 28;

/*295 | Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.*/

-- investigate the interviews
SELECT id, name, transcript FROM interviews WHERE year = 2020 AND month = 07 AND day = 28;

/*
probably related to something different
158 | Jose | “Ah,” said he, “I forgot that I had not seen you for some weeks.
It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”
159 | Eugene | “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”
160 | Barbara | “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.”
He looked from one to the other of us, as if uncertain which to address.

relevant interviews
161 | Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
162 | Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse,
I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
163 | Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket.*/

-- Ok, we need to check the courthouse parking at around 10:25, early flights on the 29th, phone calls at around 10:15 and the ATM of Fifer street in the early morning on the 28th

SELECT id, license_plate, activity, minute FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 and minute <= 25;

/*
id | license_plate | activity | minute
260 | 5P2BI95 | exit | 16
261 | 94KL13X | exit | 18
262 | 6P58WS2 | exit | 18
263 | 4328GD8 | exit | 19
264 | G412CB7 | exit | 20
265 | L93JTIZ | exit | 21
266 | 322W7JE | exit | 23
267 | 0NTHK55 | exit | 23
*/

SELECT id, caller, receiver, duration FROM phone_calls WHERE year= 2020 AND month = 7 AND day = 28 AND duration < 60;

/*
id | caller | receiver | duration
221 | (130) 555-0289 | (996) 555-8899 | 51
224 | (499) 555-9472 | (892) 555-8872 | 36
233 | (367) 555-5533 | (375) 555-8161 | 45
251 | (499) 555-9472 | (717) 555-1342 | 50
254 | (286) 555-6063 | (676) 555-6554 | 43
255 | (770) 555-1861 | (725) 555-3243 | 49
261 | (031) 555-6622 | (910) 555-3251 | 38
279 | (826) 555-1652 | (066) 555-9701 | 55
281 | (338) 555-6650 | (704) 555-2131 | 54
*/

SELECT id, account_number, transaction_type, amount FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street";

/*
id | account_number | transaction_type | amount
246 | 28500762 | withdraw | 48
264 | 28296815 | withdraw | 20
266 | 76054385 | withdraw | 60
267 | 49610011 | withdraw | 50
269 | 16153065 | withdraw | 80
275 | 86363979 | deposit | 10
288 | 25506511 | withdraw | 20
313 | 81061156 | withdraw | 30
336 | 26013199 | withdraw | 35
*/

-- now, let's check who used the phone on this day, the parking in the certain timeframe and the atm at fifer street

SELECT p.name FROM people p INNER JOIN bank_accounts b ON (p.id = b.person_id)
WHERE b.account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street")
AND p.phone_number IN (SELECT caller FROM phone_calls WHERE year= 2020 AND month = 7 AND day = 28 AND duration < 60)
AND p.license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 and minute <= 25);

/*
name
Ernest
Russell
*/

-- let's check the flights

SELECT f.hour, f.minute, f.id, f.destination_airport_id FROM flights f INNER JOIN airports a ON (a.id = f.origin_airport_id)
WHERE a.city = "Fiftyville" AND year = 2020 AND month = 7 AND day = 29 AND hour < 12;

/*
hour | minute | id | destination_airport_id
8 | 20 | 36 | 4
9 | 30 | 43 | 1
*/

-- ok, the earliest flight has the flight id 36

--let's check the passengers

SELECT passport_number FROM passengers WHERE flight_id = 36;

/*
passport_number
7214083635
1695452385
5773159633
1540955065
8294398571
1988161715
9878712108
8496433585
*/

-- let's check the owners of these passports

SELECT p.name, pas.flight_id FROM people p INNER JOIN passengers pas ON (pas.passport_number = p.passport_number)
WHERE p.passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36 OR flight_id = 43) AND (name = "Ernest" OR name = "Russell");

/*
name | flight_id
Ernest | 36
*/

-- it seems Ernest is the thief

-- check who is accomplice is and to which city he went

SELECT a.city FROM airports a INNER JOIN flights f ON (f.destination_airport_id = a.id) WHERE f.id = 36;

/*
city
London
*/

SELECT name FROM people
WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year= 2020 AND month = 7 AND day = 28 AND duration < 60
AND caller = (SELECT phone_number FROM people WHERE name = "Ernest"));

/*
name
Berthold
*/



