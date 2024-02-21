# Tests of Analysis Program

## Automated tests
Tests can be run using `pytest`. I have included tests to check for the correct datatype of the DataFrame, as well as the shape of the resulting DataFrame.

## Non-automated tests
- Manually inspect the generated plots (both bar and scatter plots) to ensure they accurately represent the analyzed data.
- Manually check for correct labeling, axis scaling, and overall clarity of the visualizations.
- Manually trigger exceptions (e.g., by simulating network issues with rapid API calls) and verify that the error handling mechanisms work as expected. Ensure that exceptions stop further execution and are appropriately logged or displayed.
- Manually verify that the notification functionality (`notify_done()`) works as expected by triggering it and confirming that the notification is sent successfully through the specified channel: https://ntfy.sh/stephens_brs_notifier
