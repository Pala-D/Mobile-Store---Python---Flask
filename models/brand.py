from models.dbcontext import DbContext
class Brand(DbContext):
    def getBrands(self):
        sql = "SELECT * FROM production.Brand"
        return self.fetchAll(sql)
    def getBrandById(self, id):
        sql = "SELECT * FROM production.Brand WHERE BrandId = ?"
        return self.fetchOne(sql, (id, ))

    def add(self, arr):
        sql = "INSERT INTO production.Brand(BrandId, BrandName) VALUES (?, ?)"
        return self.save(sql, arr)

    def delete(self,id):
        sql = "DELETE production.Brand WHERE BrandId = ?"
        return self.save(sql, (id, ))

    def deletes(self,arr):
        sql = 'DELETE production.Brand WHERE BrandId = ?'
        return self.saveBatch(sql, arr)

    def edit(self,arr):
        sql = "UPDATE production.Brand SET BrandName = ? WHERE BrandId = ?"
        return self.save(sql, arr)

    def statisticBrand(self):
        sql = "SELECT b.BrandName, COUNT(*) FROM production.Product as p JOIN production.Brand as b on p.BrandId = b.BrandId group by b.BrandName"
        return self.fetchAll(sql)