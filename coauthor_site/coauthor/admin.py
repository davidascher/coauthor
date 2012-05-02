from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from coauthor.models import UserProfile, GroupProfile, Pad
from django.contrib.auth.models import User, Group


class PadAdmin(admin.ModelAdmin):
	pass

admin.site.register(Pad, PadAdmin)


class UserProfileInline(admin.TabularInline):
	model = UserProfile
	fk_name = 'user'
	max_num = 1

class CustomUserAdmin(UserAdmin):
	inlines = [UserProfileInline,]
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',  'is_active')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class GroupProfileInline(admin.TabularInline):
	model = GroupProfile
	fk_name = 'group'
	max_num = 1

class CustomGroupAdmin(GroupAdmin):
	inlines = [GroupProfileInline,]
	list_display = ('name', )

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
