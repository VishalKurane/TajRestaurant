CREATE TABLE UserTable (
    userid INT IDENTITY(101,1) PRIMARY KEY,
    full_name VARCHAR (255) NOT NULL,
    email VARCHAR (255) UNIQUE NOT NULL,
    phone VARCHAR (10) NOT NULL,
    password_hash VARCHAR (255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

--------------------------------------------
select * from UserTable