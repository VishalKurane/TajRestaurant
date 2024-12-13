CREATE TABLE ReservationTable (
    reservation_id INT IDENTITY(101,1) PRIMARY KEY,
	user_email VARCHAR (255) NOT NULL,
    guest_name VARCHAR (255) NOT NULL,
    guest_email VARCHAR (255) NOT NULL,
    guest_phone VARCHAR (10) NOT NULL,
	checkin_date VARCHAR (255) NOT NULL,
	checkin_time VARCHAR (255) NOT NULL,
	no_of_guest INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

--------------------------------------------
select * from ReservationTable