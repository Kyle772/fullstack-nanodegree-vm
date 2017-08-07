import psycopg2 as psql


def psqlStmt(dbname="news", statement="", cols={}, *args, **kwargs):
    conn = psql.connect("dbname=" + dbname)
    cursor = conn.cursor()

    cursor.execute(statement)

    results = cursor.fetchall()

    for line in results:
        if line[1] >= 1:
            count = 0
            for section in line:
                print(("    " if count >= 1 else "") +
                      str(section) + " " +
                      (cols[str(count)])
                      )
                count += 1
    print("\n")

    conn.close()
    return results

# 1. What are the most popular three articles of all time?
psqlStmt(statement="""
    select articles.title,
        count(status) as c
    from log,
        articles
    where status like '200 OK' and
        log.path like '%' || articles.slug
    group by articles.title
    order by c desc
    limit 3;
""", cols={"0": "", "1": "views"})

# 2. Who are the most popular article authors of all time?
psqlStmt(statement="""
    select authors.name,
        count(status) as c
    from log,
        authors,
        articles
    where status like '200 OK' and
        log.path like '%' || articles.slug and
        authors.id = articles.author
    group by authors.name
    order by c desc
    limit 3;
""", cols={"0": "", "1": "views"})

# 3. On which days did more than 1% of requests lead to errors?
psqlStmt(statement="""
    select
            (extract(year from log.time),
            extract(month from log.time),
            extract(day from log.time))
        as date,
            case when
                (
                sum(case when
                    log.status like '4__%' or
                    log.status like '3__%'
                    then 1 else 0
                end)
                /
                    count(log.status)::float
                )
                > .01 then 1 else 0
            end
        as problem,
            sum(case when
                log.status like '4__%' or
                log.status like '3__%'
                then 1 else 0
                end)
            / count(log.status)::float
        as perc
    from log
    group by date
    order by perc desc
""", cols={"0": "", "1": "Problem Day", "2": "Percentage Failure"})
