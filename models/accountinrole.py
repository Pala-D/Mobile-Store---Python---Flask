from models.dbcontext import DbContext

class AccountInRole(DbContext):
    def add(self, arr):
        sql = "{CALL AddAccountInRole(?,?)}"
        return self.save(sql, arr)

    def getRoleByAccount(self, id):
        sql = "Select RoleId FROM AccountInRole WHERE AccountId = ? AND IsDeleted = 0"
        return self.fetchAll(sql, (id, ))