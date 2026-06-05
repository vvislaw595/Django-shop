# fix_admin_tables.py
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Shop.settings')
django.setup()

from django.db import connection


def fix_admin_tables():
    """修复Admin相关的表"""

    with connection.cursor() as cursor:
        # 1. 检查django_admin_log表是否存在
        cursor.execute("SHOW TABLES LIKE 'django_admin_log'")
        if not cursor.fetchone():
            print("django_admin_log表不存在，正在创建...")
            cursor.execute("""
                           CREATE TABLE django_admin_log
                           (
                               id              int AUTO_INCREMENT PRIMARY KEY,
                               action_time     datetime(6) NOT NULL,
                               object_id       longtext,
                               object_repr     varchar(200) NOT NULL,
                               action_flag     smallint unsigned NOT NULL,
                               change_message  longtext     NOT NULL,
                               content_type_id int,
                               user_id         int          NOT NULL,
                               FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
                               FOREIGN KEY (user_id) REFERENCES user (id)
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                           """)
            print("✅ django_admin_log表创建成功")
        else:
            print("✅ django_admin_log表已存在")

        # 2. 检查外键约束
        print("\n检查外键约束...")

        # 检查django_content_type表
        cursor.execute("SHOW TABLES LIKE 'django_content_type'")
        if not cursor.fetchone():
            print("❌ django_content_type表不存在，创建中...")
            cursor.execute("""
                           CREATE TABLE django_content_type
                           (
                               id        int AUTO_INCREMENT PRIMARY KEY,
                               app_label varchar(100) NOT NULL,
                               model     varchar(100) NOT NULL,
                               UNIQUE KEY (app_label, model)
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                           """)
            print("✅ django_content_type表创建成功")

        # 3. 检查user表中的id字段是否存在
        cursor.execute("DESCRIBE user")
        columns = [row[0] for row in cursor.fetchall()]
        if 'id' not in columns:
            print("❌ user表没有id字段，添加中...")
            cursor.execute("ALTER TABLE user ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST")
            print("✅ 添加id字段成功")

        # 4. 检查auth_user_groups表
        cursor.execute("SHOW TABLES LIKE 'auth_user_groups'")
        if not cursor.fetchone():
            print("❌ auth_user_groups表不存在，创建中...")
            cursor.execute("""
                           CREATE TABLE auth_user_groups
                           (
                               id       bigint AUTO_INCREMENT PRIMARY KEY,
                               user_id  int NOT NULL,
                               group_id int NOT NULL,
                               UNIQUE KEY (user_id, group_id),
                               FOREIGN KEY (user_id) REFERENCES user (id),
                               FOREIGN KEY (group_id) REFERENCES auth_group (id)
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                           """)
            print("✅ auth_user_groups表创建成功")

        # 5. 检查auth_user_user_permissions表
        cursor.execute("SHOW TABLES LIKE 'auth_user_user_permissions'")
        if not cursor.fetchone():
            print("❌ auth_user_user_permissions表不存在，创建中...")
            cursor.execute("""
                           CREATE TABLE auth_user_user_permissions
                           (
                               id            bigint AUTO_INCREMENT PRIMARY KEY,
                               user_id       int NOT NULL,
                               permission_id int NOT NULL,
                               UNIQUE KEY (user_id, permission_id),
                               FOREIGN KEY (user_id) REFERENCES user (id),
                               FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
                           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                           """)
            print("✅ auth_user_user_permissions表创建成功")

        # 6. 插入默认的内容类型
        print("\n插入默认内容类型...")
        apps_models = [
            ('user', 'user'),
            ('user', 'useraddress'),
            # 添加你的其他模型
        ]

        for app_label, model in apps_models:
            cursor.execute("""
                           INSERT
                           IGNORE INTO django_content_type (app_label, model)
                VALUES (
                           %s,
                           %s
                           )
                           """, (app_label, model))

        print("✅ 内容类型插入完成")

    print("\n🎉 Admin表修复完成！")


if __name__ == "__main__":
    fix_admin_tables()