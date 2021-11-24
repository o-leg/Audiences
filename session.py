from models import User, Audience, Reservation, Session

s = Session()

user = User(name = "batman23", surname = "Peter", username="Parker", password = "12345678")
user1 = User(name = "superman23", surname = "Peter", username="Parker", password = "12345678")
audience = Audience(number = 5432, amount_of_places = 6, status= 1)
audience1 = Audience(number = 5432, amount_of_places = 6, status= 1)
reservation = Reservation(user_id= 1, title = "Math", audience_id =1, from_date ='2021-10-21', to_date = '2021-10-22 10:00:00')
reservation1 = Reservation(user_id= 2, title = "English", audience_id =2, from_date ='2021-10-23', to_date = '2021-10-25 11:00:00')
s.add(user)
s.add(audience)
s.add(reservation)
s.add(user1)
s.add(audience1)
s.add(reservation1)

s.commit()
s.close()