# What the checks expect

Each item below is a rule the program breaks today. The test named with its ID fails until the rule
holds. In module 3 you rewrite these rules as acceptance criteria in "When X, the system shall Y"
form, each with a verify command, before Claude Code changes any code.

| ID | Module | Rule | Test |
|---|---|---|---|
| F1 | 1 | A form counts for its indicator however its template name is capitalized or spaced ("daily report", "DAILY REPORT - copy"). | `test_flaw_F1_*` |
| F7 | 2 | The Crewbook API key comes from the `CREWBOOK_API_KEY` environment variable. If it is missing, the program stops with a message naming that variable. No key appears in the code. | `test_flaw_F7_*` |
| F2 | 3 | Everything from one Monday-to-Sunday week gets the same week label, even when the week spans two months. | `test_flaw_F2_*` |
| F3 | 4 | Forms and attachments are read over the same window: the 14 days before the report date. | `test_flaw_F3_*` |
| F6 | 4 | When the API returns a list in pages, every page is read. | `test_flaw_F6_*` |
| F4 | 5 | When the API fails for a project, the report lists that project as skipped. It never shows the project with zero counts. | `test_flaw_F4_*` |
| F8 | 6 | A project's counts include only that project's attachments. | `test_flaw_F8_*` |
| F5 | 7 | Every value in the CSV sits under its own column header. | `test_flaw_F5_*` |

Rules the program already keeps, with tests that pass from the start: drafts never count; templates
unrelated to an indicator never count; folder names match in any capitalization.
