from Model import User, Audience, Reservation, Session

s = Session()

user = User(id = 1, name = "guy", surname = "girl", username="test", password = "12345678")
user1 = User(id = 2, name = "girl", surname = "guy", username="nottest", password = "12345678")
audience = Audience(id = 1, number = 5432, amount_of_places = 6, status= 1, reservuation_date= '2021-10-21')
audience1 = Audience(id = 2, number = 5432, amount_of_places = 6, status= 1, reservuation_date= '1039-09-21')
reservation = Reservation(id= 1,user_id= 1, title = "Math", audience_id =1, date ='2021-10-21')
reservation1 = Reservation(id= 2,user_id= 2, title = "English", audience_id =2, date ='2021-10-22')
s.add(user)
s.add(audience)
s.add(reservation)
s.add(user1)
s.add(audience1)
s.add(reservation1)

s.commit()
s.close()