class UserController:
    def __init__(self, db_controller):
        self.db = db_controller

    def users_list_context(self):
        users = self.db.get_all_users()
        return {
            "title": "Пользователи",
            "users": users
        }

    def user_detail_context(self, user_id):
        user = self.db.get_user_by_id(user_id)
        if not user:
            return None
            
        subs = self.db.get_user_subscriptions(user_id)
        return {
            "title": f"Пользователь {user.name}",
            "user": user,
            "subscriptions": subs
        }