SELECT 
    fullVisitorId AS user_id,
    visitId AS session_id,
    PARSE_DATE('%Y%m%d', date) AS session_date,
    device.deviceCategory AS device_category,
    trafficSource.medium AS traffic_source,
    totals.pageviews AS total_pageviews,
    totals.timeOnSite AS session_duration_seconds
FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE 
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170801';

SELECT
    fullVisitorId AS user_id,
    visitId AS session_id,
    h.eventInfo.eventAction AS event_action,
    p.v2ProductName AS product_name,
    p.productCategory AS product_category,
    (p.productPrice / 1000000) AS product_price_usd
FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS h,
    UNNEST(h.product) AS p
WHERE 
    h.type = 'EVENT'
    AND h.eventInfo.eventAction IN ('Add to Cart', 'Completed Purchase');