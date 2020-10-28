import xadmin
from xadmin import views
from .models import Banner, Nav


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "路飞学城"  # 设置站点标题
    site_footer = "路飞学城有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


# 注册轮播图模型到xadmin中
class BannerModelAdmin(object):
    list_display = ["title", "orders", "is_show"]


xadmin.site.register(Banner, BannerModelAdmin)


# 导航菜单
class NavModelAdmin(object):
    list_display = ["title", "link", "is_show", "is_site", "position"]


xadmin.site.register(Nav, NavModelAdmin)
