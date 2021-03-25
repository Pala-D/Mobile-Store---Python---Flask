from models.dbcontext import DbContext

class Category(DbContext):
    def getCategories(self):
        sql = "SELECT * FROM production.Category"
        return self.fetchAll(sql)
    
    def getCategoryById(self, id):
        sql = "SELECT * FROM production.Category WHERE CategoryId = ?"
        return self.fetchOne(sql, (id, ))

    def add(self, arr):
        sql = "INSERT INTO production.Category(CategoryId, CategoryName) VALUES (?, ?)"
        return self.save(sql, arr)

    def delete(self,id):
        sql = "DELETE production.Category WHERE CategoryId = ?"
        return self.save(sql, (id, ))

    def deletes(self,arr):
        sql = 'DELETE production.Category WHERE CategoryId = ?'
        return self.saveBatch(sql, arr)

    def edit(self,arr):
        sql = "UPDATE production.Category SET CategoryName = ? WHERE CategoryId = ?"
        return self.save(sql, arr)

    def statisticCategory(self):
        sql = "SELECT c.CategoryName, COUNT(*) FROM production.Product as p JOIN production.Category as c on p.CategoryId = c.CategoryId group by c.CategoryName"
        return self.fetchAll(sql)

