--administrator
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'tennis_admin') THEN
        CREATE ROLE tennis_admin LOGIN PASSWORD 'AdminPass123';
    END IF;
END $$;
GRANT ALL PRIVILEGES ON DATABASE stores TO tennis_admin;

--coach that can view a schedule
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'tennis_coach_user') THEN
        CREATE ROLE tennis_coach_user LOGIN PASSWORD 'CoachPass123';
    END IF;
END $$;
GRANT CONNECT ON DATABASE stores TO tennis_coach_user;
GRANT USAGE ON SCHEMA public TO tennis_coach_user;
GRANT SELECT ON tennis_schedule_view TO tennis_coach_user;

--accountant
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'tennis_accountant') THEN
        CREATE ROLE tennis_accountant LOGIN PASSWORD 'MoneyPass123';
    END IF;
END $$;
GRANT CONNECT ON DATABASE stores TO tennis_accountant;
GRANT USAGE ON SCHEMA public TO tennis_accountant;
GRANT SELECT (booking_id, total_price, booking_date) ON bookings TO tennis_accountant;