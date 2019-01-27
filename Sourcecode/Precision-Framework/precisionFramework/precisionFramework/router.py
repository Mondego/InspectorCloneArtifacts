class BCBRouter:
    """
    A router to control access to BCB (BigCloneBench MySQL DB).
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read bcb.
        """
        try:
            if model.use_db == 'bcb':
                return 'bcb'
            return None
        except AttributeError:
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write bcb (should never be used).
        """
        try:
            if model.use_db == 'bcb':
                return 'bcb'
            return None
        except AttributeError:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None

