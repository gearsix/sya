# BUGS

## Legend

[ ] = Not started
[x] = Won't do
[~] = Doing
[*] = Done
- ... = Note about the above item

## List

---

**2021-07-31** [*] don't apply file numbering when song names include file number already

	- Instead file numbering is just removed from track titles using regex.

	#regex-improvement

---

**2021-06-22** [*] handle multiple timestamp regex matches
	When there are multiple matches for the timestamp regex in a line, the last match is used as the timestamp.

	Discovered that the following line causes an issue because 2019 is counted as a timestamp
	`58:18     C4C - Melted w_ Hazy Year (Chillhop Winter Essentials 2019).`
	
	#regex-improvement

---
