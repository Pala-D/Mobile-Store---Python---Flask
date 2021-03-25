from models.dbcontext import DbContext

class Account(DbContext):
    def fetch(self, sql, arr):
        v = self.fetchOne(sql, arr)
        if v:
            return {"id": v[0], "usr": v[1], "eml": v[2]}

    def getAccount(self,arr):
        sql = "SELECT AccountId, Username, Email FROM Account WHERE Username = ? AND Password = ?"
        return self.fetch(sql,arr)

    def getAccounts(self):
        sql = "SELECT * FROM Account"
        return self.fetchAll(sql)

    def getAccountById(self, id):
        sql = "SELECT * FROM Account WHERE AccountId = ?"
        return self.fetch(sql, (id, ))

    def getAccountIdBySession(self, id):
        sql = "SELECT Account.AccountId, Username, Email FROM Account JOIN Session ON Account.AccountID = Session.AccountId WHERE SessionId = ? AND IsDeleted = 0"
        return self.fetch(sql, (id, ))

    def add(self, arr):
        sql = "{CALL AddAccount(?, ?, ?, ?)}"
        return self.save(sql, arr)

    def editPassword(self, arr):
        sql = "UPDATE Account SET Password = ? WHERE AccountId = ?"
        return self.save(sql, arr)

    def delete(self, id):
        sql = "DELETE Account WHERE AccountId = ?"
        return self.save(sql, (id, ))

