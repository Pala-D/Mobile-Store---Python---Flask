from models.dbcontext import DbContext

class Role(DbContext):
    def getRoles(self):
        sql = "SELECT * FROM Role"
        return self.fetchAll(sql)

    def getRoleById(self, id):
        sql = "SELECT * FROM Role WHERE RoleId = ?"
        return self.fetchOne(sql, (id, ))

    def getRolesByAccount(self, id):
        sql = "SELECT Role.*, IIF(AccountId IS NULL, 0, 1) FROM AccountInRole RIGHT JOIN Role ON AccountInRole.RoleId = Role.RoleId AND AccountId = ? AND IsDeleted = 0"
        return self.fetchAll(sql, (id, ))

    def getRoleByAccountId(self, id):
        sql = "SELECT Role.* FROM AccountInRole RIGHT JOIN Role ON AccountInRole.RoleId = Role.RoleId WHERE AccountId = ?"
        return self.fetchOne(sql, (id, ))
        
    def add(self, arr):
        sql = "INSERT INTO Role (RoleId, RoleName) VALUES (?, ?)"
        return self.save(sql, arr)

    def edit(self, arr):
        sql = "UPDATE Role SET RoleName = ? WHERE RoleId = ?"
        return self.save(sql, arr)

    def delete(self, id):
        sql = "DELETE Role WHERE RoleId = ?"
        return self.save(sql, (id, ))

    def deletes(self, arr):
        sql = 'DELETE Role WHERE RoleId = ?'
        return self.saveBatch(sql, arr)