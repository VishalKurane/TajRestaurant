CREATE TABLE MenuTable (
    menu_id INT IDENTITY(101,1) PRIMARY KEY,
    menu_category VARCHAR (20) NOT NULL,
    menu_name VARCHAR (100) UNIQUE NOT NULL,
    menu_description TEXT DEFAULT 'No description available',
    menu_price DECIMAL(7,2) NOT NULL DEFAULT 0.00,
    image_url VARCHAR (2083) DEFAULT 'https://dummyimage.com/150x150/000000/000000.png&text=Black+Square'
);

--------------------------------------------

select * from MenuTable
