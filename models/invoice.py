from models.dbcontext import DbContext

class Invoice(DbContext):
    def add(self, arr):
        sql = "{CALL AddInvoice(?,?,?,?,?)}"
        return self.save(sql, arr)
