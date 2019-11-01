#!/usr/bin/env bash

# copied from https://stackoverflow.com/a/47944496
curl_time() {
    curl -so /dev/null -w " \
   namelookup:  %{time_namelookup}s\n \
      connect:  %{time_connect}s\n \
   appconnect:  %{time_appconnect}s\n \
  pretransfer:  %{time_pretransfer}s\n \
     redirect:  %{time_redirect}s\n \
starttransfer:  %{time_starttransfer}s\n \
-------------------------\n \
        total:  %{time_total}s\n" "$@"
}

echo ""
echo "/elapsed_time"
echo "-------------"
curl_time "http://0.0.0.0:5000/elapsed_time?timestamp=1571356830600"

echo ""
echo "/rows_per_second"
echo "----------------"
curl_time "http://0.0.0.0:5000/rows_per_second?start_timestamp=1571356830600&finish_timestamp=1571961491664"

echo ""
echo "/rows_per_thread"
echo "----------------"
curl_time "http://0.0.0.0:5000/rows_per_thread?start_timestamp=1571356830600&finish_timestamp=1571961491664"

echo ""
echo "/thread_per_second"
echo "----------------"
curl_time "http://0.0.0.0:5000/thread_per_second?start_timestamp=1571356830600&finish_timestamp=1571961491664"
