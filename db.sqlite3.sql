BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(80) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"first_name"	varchar(30) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "user_logging" (
	"id"	integer NOT NULL,
	"date"	datetime NOT NULL,
	"aciklama"	varchar(100) NOT NULL,
	"user_id"	integer NOT NULL,
	"log_type"	varchar(20) NOT NULL,
	"status"	varchar(3),
	"type_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_departments" (
	"id"	integer NOT NULL,
	"department_number"	varchar(150) NOT NULL UNIQUE,
	"title"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_problemstatu" (
	"id"	integer NOT NULL,
	"title"	varchar(30) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_rootcause" (
	"id"	integer NOT NULL,
	"title"	varchar(30) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_problems" (
	"id"	integer NOT NULL,
	"created_date"	datetime NOT NULL,
	"closed_date"	datetime,
	"created_user_id"	integer NOT NULL,
	"order_id"	integer NOT NULL,
	"root_cause_id"	integer,
	"statu_id"	integer NOT NULL,
	"solution"	text,
	"description"	text,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("root_cause_id") REFERENCES "order_rootcause"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("created_user_id") REFERENCES "user_employee"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("order_id") REFERENCES "order_order"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("statu_id") REFERENCES "order_problemstatu"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_reservation" (
	"id"	integer NOT NULL,
	"start_date"	datetime NOT NULL,
	"end_date"	datetime NOT NULL,
	"version"	integer NOT NULL,
	"description"	varchar(100),
	"order_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("order_id") REFERENCES "order_order"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_vehicle" (
	"id"	integer NOT NULL,
	"type_name"	varchar(10) NOT NULL,
	"type_id"	varchar(10) NOT NULL,
	"description"	varchar(50),
	"active"	bool NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_reservationvehicle" (
	"id"	integer NOT NULL,
	"reservation_id"	integer NOT NULL,
	"vehicle_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("reservation_id") REFERENCES "order_reservation"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vehicle_id") REFERENCES "order_vehicle"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_orderstatu" (
	"id"	integer NOT NULL,
	"number"	integer NOT NULL,
	"aciklama"	varchar(50),
	"title"	varchar(50) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_reservationperson" (
	"id"	integer NOT NULL,
	"reservation_id"	integer NOT NULL,
	"employee_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("reservation_id") REFERENCES "order_reservation"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("employee_id") REFERENCES "user_employee"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_workflow" (
	"id"	integer NOT NULL,
	"department"	varchar(10) NOT NULL,
	"revision"	integer NOT NULL,
	"approve_user_id"	integer,
	"completed_user_id"	integer,
	"status_id"	integer NOT NULL,
	"created_date"	datetime NOT NULL,
	"planed_date"	datetime,
	"completed_date"	datetime,
	"order_id"	integer NOT NULL,
	"comment"	varchar(50) NOT NULL,
	"started_date"	datetime,
	"fisNo"	integer,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("status_id") REFERENCES "order_orderstatu"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("order_id") REFERENCES "order_order"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_customer" (
	"id"	integer NOT NULL,
	"customer_name"	varchar(50) NOT NULL,
	"telephone"	varchar(50) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"active"	varchar(1) NOT NULL,
	"created_date"	datetime NOT NULL,
	"vergi_no"	integer,
	"customer_type"	varchar(10) NOT NULL,
	"vergi_dairesi"	varchar(70) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_orderproducts" (
	"id"	integer NOT NULL,
	"amount"	integer NOT NULL,
	"order_id"	integer NOT NULL,
	"product_id"	integer NOT NULL,
	"colour"	varchar(20) NOT NULL,
	"birim_fiyat"	integer NOT NULL,
	"toplam_tutar"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("order_id") REFERENCES "order_order"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("product_id") REFERENCES "order_product"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_sube" (
	"id"	integer NOT NULL,
	"title"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user_yetenek" (
	"id"	integer NOT NULL,
	"title"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user_employee_yetenek" (
	"id"	integer NOT NULL,
	"employee_id"	integer NOT NULL,
	"yetenek_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("yetenek_id") REFERENCES "user_yetenek"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("employee_id") REFERENCES "user_employee"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_yetki" (
	"id"	integer NOT NULL,
	"title"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user_yetkilendirme" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_address" (
	"id"	integer NOT NULL,
	"ulke"	varchar(30) NOT NULL,
	"il"	varchar(30) NOT NULL,
	"ilce"	varchar(30) NOT NULL,
	"adres"	varchar(100) NOT NULL,
	"map_link"	varchar(100) NOT NULL,
	"customer_id"	integer NOT NULL,
	"active"	bool NOT NULL,
	"aciklama"	varchar(10) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("customer_id") REFERENCES "order_customer"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_order" (
	"id"	integer NOT NULL,
	"content"	text NOT NULL,
	"create_date"	datetime NOT NULL,
	"order_image"	varchar(100),
	"customer_id"	integer NOT NULL,
	"order_type"	varchar(1) NOT NULL,
	"statu_id"	integer NOT NULL,
	"stok"	varchar(1) NOT NULL,
	"iskonto"	integer NOT NULL,
	"tahmini_tarih_max"	date,
	"tahmini_tarih_min"	date,
	"sevk_adres_id"	integer,
	"satis_kanali"	varchar(10) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("statu_id") REFERENCES "order_orderstatu"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("customer_id") REFERENCES "order_customer"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("sevk_adres_id") REFERENCES "order_address"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_employee" (
	"id"	integer NOT NULL,
	"department_id"	integer NOT NULL,
	"user_id"	integer NOT NULL UNIQUE,
	"telephone"	varchar(30) NOT NULL,
	"role"	varchar(20) NOT NULL,
	"sube_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("department_id") REFERENCES "user_departments"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("sube_id") REFERENCES "user_sube"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_product" (
	"id"	integer NOT NULL,
	"product_name"	varchar(20) NOT NULL,
	"montaj_sabiti"	integer NOT NULL,
	"created_date"	datetime NOT NULL,
	"active"	bool NOT NULL,
	"product_type"	varchar(15) NOT NULL,
	"marka"	varchar(15) NOT NULL,
	"title"	varchar(150) NOT NULL UNIQUE,
	"unit"	varchar(10) NOT NULL,
	"birim_fiyat"	integer NOT NULL,
	"product_category_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("product_category_id") REFERENCES "order_productcategory"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order_productcategory" (
	"id"	integer NOT NULL,
	"title"	varchar(150) NOT NULL UNIQUE,
	"main_category"	varchar(2) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "user_logging_user_id_109b932b" ON "user_logging" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "order_problems_created_user_id_a0c13796" ON "order_problems" (
	"created_user_id"
);
CREATE INDEX IF NOT EXISTS "order_problems_order_id_1a6a2b1e" ON "order_problems" (
	"order_id"
);
CREATE INDEX IF NOT EXISTS "order_problems_root_cause_id_eb2465c0" ON "order_problems" (
	"root_cause_id"
);
CREATE INDEX IF NOT EXISTS "order_problems_statu_id_58e1a57d" ON "order_problems" (
	"statu_id"
);
CREATE INDEX IF NOT EXISTS "order_reservation_order_id_2b4f6e75" ON "order_reservation" (
	"order_id"
);
CREATE INDEX IF NOT EXISTS "order_reservationvehicle_reservation_id_812212c1" ON "order_reservationvehicle" (
	"reservation_id"
);
CREATE INDEX IF NOT EXISTS "order_reservationvehicle_vehicle_id_fed8596f" ON "order_reservationvehicle" (
	"vehicle_id"
);
CREATE INDEX IF NOT EXISTS "order_reservationperson_reservation_id_fb2ac221" ON "order_reservationperson" (
	"reservation_id"
);
CREATE INDEX IF NOT EXISTS "order_reservationperson_employee_id_f9a5977a" ON "order_reservationperson" (
	"employee_id"
);
CREATE INDEX IF NOT EXISTS "order_workflow_status_id_6bce6c54" ON "order_workflow" (
	"status_id"
);
CREATE INDEX IF NOT EXISTS "order_workflow_order_id_89372082" ON "order_workflow" (
	"order_id"
);
CREATE INDEX IF NOT EXISTS "order_orderproducts_order_id_55be4b9d" ON "order_orderproducts" (
	"order_id"
);
CREATE INDEX IF NOT EXISTS "order_orderproducts_product_id_68076fae" ON "order_orderproducts" (
	"product_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_employee_yetenek_employee_id_yetenek_id_a915f80f_uniq" ON "user_employee_yetenek" (
	"employee_id",
	"yetenek_id"
);
CREATE INDEX IF NOT EXISTS "user_employee_yetenek_employee_id_1d029f0f" ON "user_employee_yetenek" (
	"employee_id"
);
CREATE INDEX IF NOT EXISTS "user_employee_yetenek_yetenek_id_5cd53dfc" ON "user_employee_yetenek" (
	"yetenek_id"
);
CREATE INDEX IF NOT EXISTS "user_yetkilendirme_user_id_496e9774" ON "user_yetkilendirme" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "order_address_customer_id_862c0d62" ON "order_address" (
	"customer_id"
);
CREATE INDEX IF NOT EXISTS "order_order_customer_id_5bbbd957" ON "order_order" (
	"customer_id"
);
CREATE INDEX IF NOT EXISTS "order_order_statu_id_538578b4" ON "order_order" (
	"statu_id"
);
CREATE INDEX IF NOT EXISTS "order_order_sevk_adres_id_6122607c" ON "order_order" (
	"sevk_adres_id"
);
CREATE INDEX IF NOT EXISTS "user_employee_department_id_a5759ce0" ON "user_employee" (
	"department_id"
);
CREATE INDEX IF NOT EXISTS "user_employee_sube_id_a1b8b0e0" ON "user_employee" (
	"sube_id"
);
CREATE INDEX IF NOT EXISTS "order_product_product_category_id_45fe228a" ON "order_product" (
	"product_category_id"
);
COMMIT;
