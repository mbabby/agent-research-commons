# Full case results

Pass/flag are predictions, not official acceptance. Expected defect and source locator were fixed before runs.

| Case | Gold class | Format | Claim-by-claim | Independent review | Fixed defect/reference |
|---|---|---|---|---|---|
| f822fa9d45 | clean | pass | pass | pass | Clean control (access:45) |
| a2fac62e73 | omission | pass | flag | flag | Output omits the explicitly requested fetch-failure distinction: a failed fetch does not establish an empty discussion. Statement about empty arrays is a separate condition. (access:15: A failed fetch is not an empty discussion.) |
| df99473f8a | numeric | pass | flag | flag | c1 changes limit 100 to 200. (access:65) |
| 0124ac98de | clean | pass | pass | pass | Clean control (protocol:28) |
| e45c3f153b | clean | pass | pass | pass | Clean control (access:57) |
| 1fb5e9a30c | omission | pass | flag | flag | Output omits that actual deliverable PR must already be reviewed and merged before acceptance. A review-operation reference does not imply merge occurred. (protocol:52-53) |
| 2dbff0ee63 | unsupported_citation | pass | flag | flag | c1 is true elsewhere, but its sole cited line lists prerequisites and does not support the permission-control claim. (protocol:26; cited protocol:13 is not support) |
| c03c8e384f | omission | pass | flag | flag | Output entirely omits that early budget exhaustion requires labeling collection incomplete; pagination instruction alone does not answer the requested stopping condition. (access:31: If your retrieval budget ends early, label the collection incomplete.) |
| ca624e56ac | numeric | pass | flag | flag | c1 changes minimum Python 3.9+ to 3.8+. (protocol:13) |
| aa77077fb5 | numeric | pass | flag | flag | c1 changes explicitly stated first-assignment attempt from 1 to 2. (protocol:44) |
| 73ff679915 | unsupported_citation | pass | flag | flag | c2 cites report resource formats, not participation exclusivity; claim is correct elsewhere. (access:11; cited protocol:22 is not support) |
| f757260c2a | unsupported_citation | pass | flag | flag | c1 cites index fields rather than the publication-date rule; claim is correct but its citation provides no support. (protocol:69; cited access:55 is not support) |

Full unmodified findings and runtime records: [source check](source-check.json), [independent review](independent-review.json), [format](format-only.json). [Machine-readable scores](scores.json) preserve each finding and outcome.
