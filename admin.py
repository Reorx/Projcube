# admin config & register
# treated it as config file like config.py

ADMIN_INNER_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
]

from django.contrib import admin
from proj.models import Proj, Task

def register_inner():
    """
    copy from django.contrib.admin.autodiscover
    """

    import copy
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in ADMIN_INNER_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(admin.site._registry)
            import_module('%s.admin' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            admin.site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'admin'):
                raise

def register_custom():
    pass

def register_custom_with_no_option():
    from django.db.models import get_models
    from base.models import BaseRModel
    class BaseRAdmin(admin.ModelAdmin):
        exclude = ('nid', 'uid', )

    for i in get_models():
        if not i.__module__.startswith('django.'):
            admin.site.register(i)

def autoregister():

    register_inner()

    register_custom_with_no_option()



