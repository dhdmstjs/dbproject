-- Making Airlines
insert into airline values("American Airlines");
insert into airline values("China Eastern");
insert into airline values("Delta");
insert into airline values("Korean Air");

-- Making Airports
insert into airport values("JFK", "New York");
insert into airport values("ORD", "Chicago");
insert into airport values("LHR", "London");
insert into airport values("ATL", "Atlanta");
insert into airport values("CDG", "Paris");
insert into airport values("PEK", "Beijing");
insert into airport values("PVG", "Shanghai");

-- Making Airplanes
insert into airplane values("Delta", "12345", 200);
insert into airplane values("Delta", "11111", 100);
insert into airplane values("China Eastern", "12345", 200);
insert into airplane values("China Eastern", "54321", 150);
insert into airplane values("Korean Air", "56789", 60);
insert into airplane values("Korean Air", "22222", 160);
insert into airplane values("American Airlines", "33322", 220);
insert into airplane values("American Airlines", "00000", 120);
insert into airplane values("American Airlines", "11111", 60);

-- Making Flights
insert into flight values("Delta", "98765", "JFK", "2018-05-11 12:00", "ORD", "2018-05-11 18:00", 200.20, "on-time", "12345");
insert into flight values("Delta", "12321", "ATL", "2018-04-11 10:30", "JFK", "2018-04-11 13:00", 150.00, "landed", "11111");
insert into flight values("China Eastern", "12121", "PEK", "2018-06-05 18:00", "ORD", "2018-06-05 21:00", 330.00, "on-time", "12345");
insert into flight values("China Eastern", "98765", "PVG", "2018-02-10 12:00", "JFK", "2018-05-11 14:00", 940.33, "landed", "54321");
insert into flight values("Korean Air", "22234", "CDG", "2019-01-10 6:00", "LHR", "2019-01-10 10:00", 400.00, "on-time", "56789");
insert into flight values("Korean Air", "43434", "JFK", "2018-09-11 10:35", "CDG", "2018-9-11 19:40", 800.10, "on-time", "22222");
insert into flight values("American Airlines", "99888", "ORD", "2018-12-30 20:00", "LHR", "2018-12-31 00:20", 525.99, "on-time", "33322");
insert into flight values("American Airlines", "00011", "JFK", "2018-06-12 21:40", "ATL", "2018-06-12 23:40", 180.50, "on-time", "33322");
insert into flight values("American Airlines", "54321", "ATL", "2018-06-13 02:10", "CDG", "2018-06-13 13:20", 910.33, "on-time", "00000");
insert into flight values("American Airlines", "01010", "ORD", "2018-08-05 12:20", "PVG", "2018-08-06 06:00", 1200.20, "on-time", "11111");

-- Making Tickets
insert into ticket values("00001", "Delta", "98765");
insert into ticket values("00202", "Delta", "98765");
insert into ticket values("00013", "Delta", "98765");
insert into ticket values("09004", "Delta", "98765");
insert into ticket values("02005", "Delta", "98765");
insert into ticket values("00401", "Delta", "12321");
insert into ticket values("00602", "Delta", "12321");
insert into ticket values("00903", "Delta", "12321");
insert into ticket values("00014", "Delta", "12321");
insert into ticket values("05005", "Delta", "12321");
insert into ticket values("60001", "China Eastern", "98765");
insert into ticket values("10002", "China Eastern", "98765");
insert into ticket values("34003", "China Eastern", "98765");
insert into ticket values("00424", "China Eastern", "98765");
insert into ticket values("52005", "China Eastern", "98765");
insert into ticket values("07801", "China Eastern", "12121");
insert into ticket values("01102", "China Eastern", "12121");
insert into ticket values("99003", "China Eastern", "12121");
insert into ticket values("01404", "China Eastern", "12121");
insert into ticket values("00655", "China Eastern", "12121");
insert into ticket values("00221", "Korean Air", "22234");
insert into ticket values("00402", "Korean Air", "22234");
insert into ticket values("06503", "Korean Air", "22234");
insert into ticket values("00104", "Korean Air", "22234");
insert into ticket values("52301", "Korean Air", "43434");
insert into ticket values("32202", "Korean Air", "43434");
insert into ticket values("64203", "Korean Air", "43434");
insert into ticket values("52504", "Korean Air", "43434");
insert into ticket values("11101", "American Airlines", "99888");
insert into ticket values("98702", "American Airlines", "99888");
insert into ticket values("42403", "American Airlines", "99888");
insert into ticket values("00904", "American Airlines", "99888");
insert into ticket values("15405", "American Airlines", "99888");
insert into ticket values("13101", "American Airlines", "54321");
insert into ticket values("24202", "American Airlines", "54321");
insert into ticket values("64303", "American Airlines", "54321");
insert into ticket values("64204", "American Airlines", "54321");
insert into ticket values("98705", "American Airlines", "54321");
insert into ticket values("05606", "American Airlines", "54321");
insert into ticket values("06501", "American Airlines", "01010");
insert into ticket values("03302", "American Airlines", "01010");
insert into ticket values("45303", "American Airlines", "01010");
insert into ticket values("05354", "American Airlines", "01010");
insert into ticket values("00335", "American Airlines", "01010");
insert into ticket values("00036", "American Airlines", "01010");