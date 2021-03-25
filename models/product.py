from models.dbcontext import DbContext
class Product(DbContext):
    def getProducts(self):
        sql = "SELECT * FROM production.Product"
        return self.fetchAll(sql)

    def getProductsJson(self):
        sql = "SELECT * FROM production.Product"
        a = self.fetchAll(sql)
        return [{"id": v[0], "name": v[1], "price": str(v[4]), "des": v[-1]} for v in a]

    def getProductsByCategory(self, id):
        sql = "SELECT * FROM production.Product WHERE CategoryId = ?"
        return self.fetchAll(sql, (id, ))

    def getProductsJsonByCategory(self, id):
        a = self.getProductsByCategory(id)
        b = []
        for v in a:
            b.append({"id": v[0], "name": v[1], "cid": v[3]})
        return b

    def getProductsByBrand(self, id):
        sql = "SELECT * FROM production.Product WHERE BrandId = ?"
        return self.fetchAll(sql, (id, ))

    def getProductById(self, id):
        sql = "SELECT * FROM production.Product WHERE ProductId = ?"
        return self.fetchOne(sql, (id, ))

    def getProductsRelation(self, id):
        sql = "SELECT P.* FROM production.Product as P JOIN (SELECT * FROM production.Product WHERE ProductId = ?) as M on P.BrandId = M.BrandId and P.CategoryId = M.CategoryId"
        return self.fetchAll(sql, (id, ))

    def searchProducts(self, q, page, size):
        sql = "SELECT * FROM production.Product WHERE ProductName LIKE ? ORDER BY ProductId OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        return self.fetchAll(sql, ("%" + q + "%", (page - 1)*size, size))

    def searchCount(self, q):
        sql = "SELECT COUNT(*) FROM production.Product WHERE ProductName LIKE ?"
        v = self.fetchOne(sql, ("%" + q + "%", ))
        return v[0]

    def homeCount(self):
        sql = "SELECT COUNT(*) FROM production.Product"
        cur = self.database.cursor()
        cur.execute(sql)
        v = cur.fetchone()
        cur.close()
        return v[0]

    def homeCategoryCount(self, id):
        sql = "SELECT COUNT(*) FROM production.Product WHERE CategoryId = ?"
        v = self.fetchOne(sql, (id, ))
        return v[0]

    def add(self, arr):
        sql = "INSERT INTO production.Product (ProductName, BrandId, CategoryId, Price, ImageUrl, Quantity, Description) VALUES (?, ?, ?, ?, ?, ?, ?)"
        return self.save(sql, arr)

    def delete(self, id):
        sql = "DELETE production.Product WHERE ProductId = ?"
        return self.save(sql, (id, ))

    def edit(self,arr):
        sql = "UPDATE production.Product SET ProductName = ?, BrandId =?, CategoryId = ?, Price =?, ImageUrl = ?, Quantity = ?, Description = ? WHERE ProductId = ?"
        return self.save(sql, arr)

    def getProductsForHome(self, page, size):
        sql = "SELECT * FROM production.Product ORDER BY ProductId OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        return self.fetchAll(sql, ((page - 1)*size, size))

    def getProductsByCategoryForHome(self, id, page, size):
        sql = "SELECT * FROM production.Product WHERE CategoryId = ? ORDER BY ProductId OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        return self.fetchAll(sql, (id, (page - 1)*size, size))