alter table flats
    add photo_links text;

alter table flats
    add is_tg_posted boolean default false;
