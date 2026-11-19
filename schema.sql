-- Ejecutar en Supabase > SQL Editor.
create table if not exists public.products (
 id bigint generated always as identity primary key,
 user_id uuid not null references auth.users(id) on delete cascade,
 name text not null check (char_length(trim(name)) > 0),
 quantity integer not null check (quantity >= 0),
 price numeric(12,2) not null check (price >= 0),
 created_at timestamptz not null default now()
);
create table if not exists public.access_logs (
 id bigint generated always as identity primary key,
 user_id uuid not null references auth.users(id) on delete cascade,
 event text not null check (event in ('login','logout')),
 created_at timestamptz not null default now()
);
alter table public.products enable row level security;
alter table public.access_logs enable row level security;
create policy "Read own products" on public.products for select to authenticated using ((select auth.uid()) = user_id);
create policy "Add own products" on public.products for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Delete own products" on public.products for delete to authenticated using ((select auth.uid()) = user_id);
create policy "Read own access logs" on public.access_logs for select to authenticated using ((select auth.uid()) = user_id);
create policy "Insert own access logs" on public.access_logs for insert to authenticated with check ((select auth.uid()) = user_id);
