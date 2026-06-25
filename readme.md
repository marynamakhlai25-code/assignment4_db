Розробка, наповнення та оптимізація реляційної бази даних для керування інфраструктурою тенісного клубу: гравці, тренери, корти, бронювання та матчі
## перевірка швидкості без індексу
Gather  (cost=1000.00..8320.75 rows=505 width=41) (actual time=7.087..61.105 rows=508.00 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  Buffers: shared hit=4614
  ->  Parallel Seq Scan on bookings  (cost=0.00..7270.25 rows=210 width=41) (actual time=0.067..36.014 rows=169.33 loops=3)
        Filter: (booking_date = '2024-06-15'::date)
        Rows Removed by Filter: 169831
        Buffers: shared hit=4614


#### Planning Time: 2.692 ms
#### Execution Time: 63.707 ms
СУБД прочитала 4614 сторінок пам'яті й перевірила кожен рядок вручну, відкинувши 169 831 запис на кожному з трьох потоків. Загальний час виконання склав 63.707 мс.

## перевірка швидкості з індексом
Bitmap Heap Scan on bookings  (cost=8.34..1467.64 rows=505 width=41) (actual time=0.779..3.523 rows=508.00 loops=1)
  Recheck Cond: (booking_date = '2024-06-15'::date)
  Heap Blocks: exact=476
  Buffers: shared hit=476 read=4
  ->  Bitmap Index Scan on idx_bookings_date  (cost=0.00..8.21 rows=505 width=0) (actual time=0.682..0.682 rows=508.00 loops=1)
        Index Cond: (booking_date = '2024-06-15'::date)
        Index Searches: 1
        Buffers: shared read=4
Planning:
  Buffers: shared hit=18 read=1


#### Planning Time: 2.749 ms
#### Execution Time: 4.463 ms
PostgreSQL повністю відмовився від сканування всієї таблиці.Система миттєво знайшла позиції потрібних 508 рядків у структурі індексу і зчитала лише 476 сторінок даних. Чистий час виконання впав до 4.463 мс.
