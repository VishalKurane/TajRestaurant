CREATE TRIGGER trg_UpdateDate_UserTable
ON dbo.UserTable
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE UserTable
    SET updated_at = GETDATE()
    FROM inserted
    WHERE UserTable.userid = inserted.userid;
END;

-------------------------------------------------
CREATE TRIGGER trg_UpdateDate_AdminTable
ON dbo.AdminTable
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE AdminTable
    SET updated_at = GETDATE()
    FROM inserted
    WHERE AdminTable.admin_id = inserted.admin_id;
END;

-------------------------------------------------

CREATE TRIGGER trg_UpdateDate_ReservationTable
ON dbo.ReservationTable
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE ReservationTable
    SET updated_at = GETDATE()
    FROM inserted
    WHERE ReservationTable.reservation_id = inserted.reservation_id;
END;


-------------------------------------------------

SELECT * FROM sys.triggers