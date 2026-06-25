CREATE OR REPLACE VIEW tennis_schedule_view AS
SELECT
    b.booking_id,
    p.first_name || ' ' || p.last_name AS player_name,
    cr.court_name,
    cr.surface_type,
    b.booking_date,
    b.start_time,
    COALESCE(c.first_name || ' ' || c.last_name, 'No Coach Assigned') AS coach_name,
    b.total_price
FROM bookings b
JOIN players p ON b.player_id = p.player_id
JOIN courts cr ON b.court_id = cr.court_id
LEFT JOIN coaches c ON b.coach_id = c.coach_id;
