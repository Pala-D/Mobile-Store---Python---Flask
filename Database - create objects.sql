
CREATE DATABASE MobileStore;
GO
USE MobileStore;
GO

-- create schemas
CREATE SCHEMA production;
GO

CREATE SCHEMA sales;
GO


-- create tables

CREATE TABLE Account(
	AccountId CHAR(16) NOT NULL PRIMARY KEY,
	Username VARCHAR(32) NOT NULL UNIQUE,
	Password VARBINARY(64) NOT NULL,
	Email VARCHAR(64) NOT NULL
);
GO
--select * from Account;

CREATE PROCEDURE AddAccount(
	@Id CHAR(16),
	@Usr VARCHAR(32),
	@Pwd VARBINARY(64),
	@Eml VARCHAR(64)
)AS
	
	IF NOT EXISTS (SELECT * FROM Account WHERE Username = @Usr)
		INSERT INTO Account (AccountId, Username, Password, Email) VALUES
			(@Id, @Usr, @Pwd, @Eml);
GO


CREATE TABLE Role(
	RoleId INT NOT NULL PRIMARY KEY,
	RoleName NVARCHAR(32) NOT NULL UNIQUE
);
GO
--select * from Role;


CREATE TABLE AccountInRole(
	AccountId CHAR(16) NOT NULL REFERENCES Account(AccountId),
	RoleId INT NOT NULL REFERENCES Role(RoleId),
	IsDeleted BIT NOT NULL DEFAULT 0,
	PRIMARY KEY (AccountId, RoleId)
);
GO
--select * from AccountInRole;

CREATE PROC AddAccountInRole(@aid CHAR(16), @rid INT)
AS
BEGIN
	IF EXISTS(SELECT * FROM AccountInRole WHERE AccountId = @aid AND RoleId = @rid)
		UPDATE AccountInRole SET IsDeleted = ~IsDeleted WHERE AccountId = @aid AND RoleId = @rid;
	ELSE
		INSERT INTO AccountInRole(AccountId,RoleId) VALUES (@aid,@rid);
END


CREATE TABLE Permission(
	PermissionId INT NOT NULL IDENTITY (1, 1) PRIMARY KEY,
	Permission NVARCHAR(32) NOT NULL UNIQUE,
);
GO
-- select * from Permission

CREATE TABLE PermissionInRole(
	PermissionId INT NOT NULL REFERENCES Permission(PermissionId),
	RoleId INT NOT NULL REFERENCES Role(RoleId),
	IsDeleted BIT NOT NULL DEFAULT 0,
	PRIMARY KEY (PermissionId, RoleId)
);
GO

-- select * from Session
CREATE TABLE Session(
	SessionId CHAR(32) NOT NULL PRIMARY KEY,
	AccountId CHAR(16) NOT NULL REFERENCES Account(AccountId),
	IsRemember BIT NOT NULL DEFAULT 0,
	IsDeleted BIT NOT NULL DEFAULT 0,
	CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
	UpdatedDate DATETIME NOT NULL DEFAULT GETDATE()
);
GO


CREATE TABLE production.Category (
	CategoryId INT NOT NULL PRIMARY KEY,
	CategoryName NVARCHAR (64) NOT NULL
);
GO
--select * from production.Category


CREATE TABLE production.Brand (
	BrandId INT NOT NULL PRIMARY KEY,
	BrandName VARCHAR (64) NOT NULL
);
GO

--select * from production.Brand


CREATE TABLE production.Product (
	ProductId INT NOT NULL IDENTITY (1, 1) PRIMARY KEY,
	ProductName NVARCHAR (256) NOT NULL,
	BrandId INT NOT NULL,
	CategoryId INT NOT NULL,
	Price DECIMAL (10, 0) NOT NULL,
	ImageUrl VARCHAR(128),
	Quantity SMALLINT NOT NULL,
	Description NVARCHAR(MAX),
	FOREIGN KEY (CategoryId) REFERENCES production.Category (CategoryId) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (BrandId) REFERENCES production.Brand (BrandId) ON DELETE CASCADE ON UPDATE CASCADE
);
GO
--select * from production.Product



CREATE TABLE production.Stock (
	ProductId INT NOT NULL,
	Quantity SMALLINT NOT NULL,
	PRIMARY KEY (ProductId, Quantity),
	FOREIGN KEY (ProductId) REFERENCES production.Product (ProductId) ON DELETE CASCADE ON UPDATE CASCADE
);
GO



CREATE TABLE sales.Customer (
	CustomerId INT IDENTITY (1, 1) PRIMARY KEY,
	FirstName NVARCHAR (64) NOT NULL,
	LastName NVARCHAR (128) NOT NULL,
	Phone VARCHAR (16) NOT NULL,
	Email VARCHAR (256) NOT NULL,
	Address NVARCHAR (256),
);
GO


CREATE TABLE sales.Staff (
	StaffId INT NOT NULL IDENTITY (1, 1) PRIMARY KEY,
	FirstName NVARCHAR (64) NOT NULL,
	LastName NVARCHAR (64) NOT NULL,
	Email VARCHAR (256) NOT NULL UNIQUE,
	Phone VARCHAR (16),
	ManagerId INT,
	FOREIGN KEY (ManagerId) REFERENCES sales.Staff (StaffId) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO


CREATE TABLE sales.[Order] (
	OrderId INT NOT NULL IDENTITY (1, 1) PRIMARY KEY,
	CustomerId INT,
	OrderStatus TINYINT NOT NULL,
	-- Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
	OrderDate DATETIME NOT NULL DEFAULT GETDATE(),
	RequiredDate DATE NOT NULL,
	ShippedDate DATE,
	StaffId INT NOT NULL,
	FOREIGN KEY (CustomerId) REFERENCES sales.Customer (CustomerId) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (StaffId) REFERENCES sales.Staff (StaffId) ON DELETE NO ACTION ON UPDATE NO ACTION
);
GO


CREATE TABLE sales.OrderItem (
	OrderId INT NOT NULL,
	ItemId INT NOT NULL,
	ProductId INT NOT NULL,
	Quantity SMALLINT NOT NULL,
	Price DECIMAL (10, 0) NOT NULL,
	discount DECIMAL (8, 0) NOT NULL DEFAULT 0,
	PRIMARY KEY (OrderId, ItemId),
	FOREIGN KEY (OrderId) REFERENCES sales.[Order] (OrderId) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (ProductId) REFERENCES production.Product (ProductId) ON DELETE CASCADE ON UPDATE CASCADE
);
GO


CREATE TABLE Cart (
	CartId CHAR(16) NOT NULL,
	ProductId INT NOT NULL REFERENCES production.Product(ProductId),
	Quantity SMALLINT NOT NULL,
	AddedDate DATETIME NOT NULL DEFAULT GETDATE(),
	PRIMARY KEY (CartId, ProductId)
);
-- SELECT * from Cart

CREATE TABLE Invoice(
	InvoiceId CHAR(16) NOT NULL PRIMARY KEY,
	InvoiceDate DATETIME NOT NULL DEFAULT GETDATE(),
	FullName NVARCHAR(64),
	Address NVARCHAR(128),
	Phone VARCHAR(16),
	Email VARCHAR(64)
)


CREATE TABLE InvoiceDetail(
	InvoiceId CHAR(16) NOT NULL REFERENCES Invoice(InvoiceId),
	ProductId INT NOT NULL REFERENCES production.Product(ProductId),
	Quantity SMALLINT NOT NULL,
	Price DECIMAL (10, 0) NOT NULL,
	PRIMARY KEY (InvoiceId, ProductId)
)
GO
-- select * from Invoice
-- select * from InvoiceDetail


CREATE PROC AddInvoice(
	@cartid CHAR(16),
	@fullname NVARCHAR(64),
	@address NVARCHAR(128),
	@phone VARCHAR(16),
	@email VARCHAR(64)
)
AS
BEGIN
	INSERT INTO Invoice(InvoiceId, FullName, Address, Phone, Email) VALUES (@cartid, @fullname, @address, @phone, @email)   
	INSERT INTO InvoiceDetail(InvoiceId, ProductId, Quantity, Price) SELECT @cartid, Cart.ProductId, Cart.Quantity, Price 
		FROM Cart JOIN production.Product 
		ON Cart.ProductId = production.Product.ProductId AND CartId = @cartid
END
---select * from Invoice
---select * from InvoiceDetail



CREATE PROC GetProducts
AS
	SELECT P.*, B.BrandName, C.CategoryName FROM production.Product AS P 
		JOIN production.Brand AS B ON P.BrandId = B.BrandId
		JOIN production.Category AS C ON P.CategoryId = C.CategoryId
GO



CREATE PROC AddCart(@CartId CHAR(16), @ProductId INT, @Quantity SMALLINT)
AS
BEGIN
	IF EXISTS(SELECT * FROM Cart WHERE CartId = @CartId AND ProductId = @ProductId)
		UPDATE Cart SET Quantity += @Quantity WHERE CartId = @CartId AND ProductId = @ProductId
	ELSE
		INSERT INTO Cart(CartId, ProductId, Quantity) VALUES (@CartId, @ProductId, @Quantity)
END

-- select * from Cart



CREATE TABLE Comment(
	CommentId VARCHAR(16) NOT NULL,
	Content NVARCHAR(64) NOT NULL,
	Position VARCHAR(8) NOT NULL,
	ParentId VARCHAR(16)
);

