-- to be run after python manage.py migrate, to seed data

delete from coupons_coupontype;
insert into coupons_coupontype (coupon_type) values ("single-use"),("single-use-per-user"),("multi-use"),("perpetual-use");
