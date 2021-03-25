from models.dbcontext import DbContext
class Cart(DbContext):
    def add(self, arr):
        sql = "{CALL AddCart(?, ?, ?)}"
        return self.save(sql, arr)
        
    def getCarts(self, id):
        sql = "SELECT Cart.*, Price, ImageUrl, ProductName FROM Cart JOIN production.Product ON Cart.ProductId = production.Product.ProductId AND CartId = ?"
        return self.fetchAll(sql, (id, ))

    def delete(self, arr):
        sql = "DELETE FROM Cart WHERE CartId =? AND ProductId = ?"
        return self.save(sql, arr)

    def edit(self, arr):
        sql = "UPDATE Cart SET Quantity = ? WHERE CartId = ? AND ProductId = ?"
        return self.save(sql, arr)