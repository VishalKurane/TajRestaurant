select * from MenuTable
SELECT * FROM UserTable
SELECT * FROM AdminTable
SELECT * FROM ReservationTable


INSERT INTO MenuTable (menu_category, menu_name, menu_price)
VALUES 
	('Breakfast', 'Pancake', '150'),
	('Breakfast', 'Omelette', '100')

INSERT INTO MenuTable (menu_category, menu_name,  menu_price,  image_url)
VALUES 
	('BREAKFAST', 'Poha', '100', 'https://media.istockphoto.com/id/670526200/photo/poha-indian-snacks.jpg?s=612x612&w=0&k=20&c=iEVKSfRzmcHxPIz1fKQBNzmcRpLbseh5vjXaRVckRZA=')


INSERT INTO MenuTable (menu_category, menu_name, menu_description,  menu_price,  image_url)
VALUES 
	('DESSERTS', 'Gulab Jamun', 'Include 5 Pieces' ,'120', 'https://t3.ftcdn.net/jpg/08/42/48/86/240_F_842488691_jNknbqQn2GSMXFggvtyX3UaVORtBRFSc.jpg')


INSERT INTO MenuTable (menu_category, menu_name,  menu_price,  image_url)
VALUES 
	('BREAKFAST', 'Omelette', '100', 'https://media.istockphoto.com/id/485040276/photo/herb-omelette-with-chives-and-oregano.jpg?s=612x612&w=0&k=20&c=gWzwd_-neHOmCgirxaaGCwEJElbuYPzY917oWPWp6kI='),
	('BREAKFAST', 'Pancake', '150', 'https://t4.ftcdn.net/jpg/02/19/69/91/240_F_219699121_wPsqZWnExtVLbowqsJLcueqjr5pf0uZn.jpg'),
	('LUNCH', 'Grilled Chicken', '400', 'https://media.istockphoto.com/id/496919860/photo/bbq-chicken-whole.jpg?s=612x612&w=0&k=20&c=CCoJhS4M6I1Vg-Tc5AjiqMEhxS0AFQIp90KpEvASaHU='),
	('LUNCH', 'Mixed Veg', '300', 'https://t3.ftcdn.net/jpg/06/94/29/48/240_F_694294860_p9yhvDJjP1iwezZxwGITd9WJLL4Yd5Vt.jpg'),
	('DINNER', 'Paneer Tikka Masala', '250', 'https://www.shutterstock.com/image-photo/indian-paneer-butter-masala-curry-260nw-2499932035.jpg'),
	('DINNER', 'Chicken Biryani', '180', 'https://media.istockphoto.com/id/1058029096/photo/chicken-biryani.jpg?s=612x612&w=0&k=20&c=yVV1RArkYz1fXf0Blpeuwxt0yTHHDnlOURVMJmYgAeI='),
	('DESSERTS', 'Ice Cream', '50', 'https://media.gettyimages.com/id/157472912/photo/ice-cream-composition-on-a-bowl.jpg?s=612x612&w=gi&k=20&c=AniWX1OhaarUxCkgjUoKiA3bKVllK0upCylW6Z0PCMQ='),
	('DESSERTS', 'Kulfi', '20', 'https://media.istockphoto.com/id/657090194/photo/rajwari-or-rajwadi-sweet-kesar-badam-pista-kulfi-or-ice-cream-candy.jpg?s=612x612&w=0&k=20&c=qr9qpyJKBHBy9iS9nQn-0h4f-xn6rE4TUOtXiYZwkoY='),
	('WINE CARD', 'Beer', '190', 'https://t4.ftcdn.net/jpg/09/09/73/55/360_F_909735591_wPPLrm23yJIsRnDZqKaulGEEDAVWPEQu.jpg'),
	('WINE CARD', 'Wine', '210', 'https://images.pexels.com/photos/391213/pexels-photo-391213.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'),
	('DRINKS & TEA', 'Milk Shake', '75', 'https://www.shutterstock.com/image-photo/deliciously-tempting-milkshake-topped-whipped-600nw-2464166057.jpg'),
	('DRINKS & TEA', 'Tea', '10', 'https://img.freepik.com/premium-photo/cup-tea-is-saucer-logo-says-tea_1257223-34073.jpg')


SELECT menu_category, menu_name, menu_description, menu_price, image_url FROM MenuTable


DELETE from MenuTable where menu_category = 'BREAKFAST' and menu_name= 'Poha'


UPDATE MenuTable
SET menu_category = 'HOT & COLD SIPS'
WHERE menu_category = 'DRINKS & TEA';
